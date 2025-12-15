"""
FastAPI 学习教程
================

这个文件包含了 FastAPI 的基础到进阶知识点，
运行方式: uvicorn tests.fastapi_tutorial:app --reload
访问文档: http://127.0.0.1:8000/docs (Swagger UI)
         http://127.0.0.1:8000/redoc (ReDoc)
"""

from fastapi import FastAPI, Query, Path, Body, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

# ============================================================
# 1. 创建 FastAPI 应用实例
# ============================================================
app = FastAPI(
    title="FastAPI 学习教程",
    description="一个完整的 FastAPI 学习示例",
    version="1.0.0",
)


# ============================================================
# 2. 基础路由 - GET 请求
# ============================================================
@app.get("/")
async def root():
    """最简单的根路由"""
    return {"message": "欢迎学习 FastAPI! 🚀"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """路径参数示例 - 打招呼"""
    return {"message": f"你好, {name}!"}


# ============================================================
# 3. 枚举类型参数
# ============================================================
class ModelName(str, Enum):
    """模型名称枚举"""
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """枚举路径参数示例"""
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


# ============================================================
# 4. 查询参数
# ============================================================
fake_items_db = [{"item_name": f"Item {i}"} for i in range(100)]


@app.get("/items/")
async def read_items(
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=10, ge=1, le=100, description="返回的最大记录数"),
    q: Optional[str] = Query(default=None, min_length=3, max_length=50, description="搜索关键字"),
):
    """
    查询参数示例
    - **skip**: 分页偏移量
    - **limit**: 每页数量
    - **q**: 可选的搜索关键字
    """
    items = fake_items_db[skip : skip + limit]
    if q:
        items = [item for item in items if q.lower() in item["item_name"].lower()]
    return {"items": items, "total": len(items)}


# ============================================================
# 5. Pydantic 模型 - 请求体验证
# ============================================================
class Item(BaseModel):
    """商品模型"""
    name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    description: Optional[str] = Field(default=None, max_length=500, description="商品描述")
    price: float = Field(..., gt=0, description="商品价格，必须大于0")
    tax: Optional[float] = Field(default=None, ge=0, description="税费")
    tags: List[str] = Field(default=[], description="商品标签")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "iPhone 15 Pro",
                "description": "Apple 最新款旗舰手机",
                "price": 7999.0,
                "tax": 1.5,
                "tags": ["电子产品", "手机"]
            }
        }


class ItemResponse(BaseModel):
    """商品响应模型"""
    id: int
    item: Item
    price_with_tax: Optional[float] = None


# 模拟数据库
items_db: dict[int, Item] = {}
item_id_counter = 0


@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: Item):
    """
    创建商品 - POST 请求体示例
    
    - 自动验证请求体
    - 自动生成文档
    - 自动序列化响应
    """
    global item_id_counter
    item_id_counter += 1
    items_db[item_id_counter] = item
    
    price_with_tax = item.price
    if item.tax:
        price_with_tax += item.price * item.tax
    
    return ItemResponse(
        id=item_id_counter,
        item=item,
        price_with_tax=price_with_tax
    )


@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int = Path(..., title="商品 ID", ge=1),
):
    """获取单个商品 - 路径参数验证"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    item = items_db[item_id]
    price_with_tax = item.price + (item.price * item.tax if item.tax else 0)
    
    return ItemResponse(id=item_id, item=item, price_with_tax=price_with_tax)


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int = Path(..., ge=1),
    item: Item = Body(...),
):
    """更新商品 - PUT 请求"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    items_db[item_id] = item
    price_with_tax = item.price + (item.price * item.tax if item.tax else 0)
    
    return ItemResponse(id=item_id, item=item, price_with_tax=price_with_tax)


@app.delete("/items/{item_id}")
async def delete_item(item_id: int = Path(..., ge=1)):
    """删除商品 - DELETE 请求"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    del items_db[item_id]
    return {"message": f"商品 {item_id} 已删除"}


# ============================================================
# 6. 依赖注入 (Dependency Injection)
# ============================================================
async def common_parameters(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    """公共查询参数依赖"""
    return {"q": q, "skip": skip, "limit": limit}


async def verify_token(x_token: str = Header(...)):
    """验证 Token 的依赖"""
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    """依赖注入示例 - 公共参数"""
    return {"commons": commons}


@app.get("/secure-items/")
async def read_secure_items(token: str = Depends(verify_token)):
    """依赖注入示例 - Token 验证
    
    请求时需要添加 Header: X-Token: fake-super-secret-token
    """
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]


# ============================================================
# 7. 异常处理
# ============================================================
class UnicornException(Exception):
    """自定义异常"""
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request, exc: UnicornException):
    """自定义异常处理器"""
    return JSONResponse(
        status_code=418,
        content={"message": f"哎呀！{exc.name} 做了一些事情。那里有独角兽..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    """触发自定义异常示例"""
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# ============================================================
# 8. 嵌套模型
# ============================================================
class Address(BaseModel):
    """地址模型"""
    city: str
    street: str
    zip_code: str


class User(BaseModel):
    """用户模型 - 展示嵌套模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    full_name: Optional[str] = None
    address: Optional[Address] = None
    tags: List[str] = []

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "full_name": "John Doe",
                "address": {
                    "city": "北京",
                    "street": "朝阳区某某街道",
                    "zip_code": "100000"
                },
                "tags": ["vip", "developer"]
            }
        }


@app.post("/users/", response_model=User)
async def create_user(user: User):
    """创建用户 - 嵌套模型示例"""
    return user


# ============================================================
# 9. 多个请求体参数
# ============================================================
class Offer(BaseModel):
    """报价模型"""
    name: str
    discount: float = Field(..., ge=0, le=1, description="折扣 (0-1)")


@app.post("/offers/")
async def create_offer(
    item: Item = Body(..., embed=True),
    offer: Offer = Body(..., embed=True),
):
    """多请求体参数示例"""
    final_price = item.price * (1 - offer.discount)
    return {
        "item": item,
        "offer": offer,
        "final_price": final_price,
    }


# ============================================================
# 10. 响应状态码
# ============================================================
from fastapi import status


@app.post("/login/", status_code=status.HTTP_200_OK)
async def login(username: str = Body(...), password: str = Body(...)):
    """登录示例 - 不同的响应状态码"""
    # 这只是示例，实际不要这样验证密码！
    if username == "admin" and password == "admin":
        return {"message": "登录成功", "username": username}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="用户名或密码错误",
    )


# ============================================================
# 11. 后台任务 (Background Tasks)
# ============================================================
from fastapi import BackgroundTasks


def write_notification(email: str, message: str = ""):
    """模拟发送邮件的后台任务"""
    with open("notification.log", mode="a") as log:
        log.write(f"notification for {email}: {message}\n")
    print(f"✉️ 邮件已发送到 {email}")


@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
    message: str = Body(...),
):
    """后台任务示例 - 发送通知"""
    background_tasks.add_task(write_notification, email, message)
    return {"message": "通知将在后台发送"}


# ============================================================
# 运行说明
# ============================================================
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                FastAPI 学习教程                          ║
    ╠══════════════════════════════════════════════════════════╣
    ║  运行方式:                                               ║
    ║  uvicorn tests.fastapi_tutorial:app --reload             ║
    ║                                                          ║
    ║  访问地址:                                               ║
    ║  • API: http://127.0.0.1:8000                            ║
    ║  • Swagger 文档: http://127.0.0.1:8000/docs              ║
    ║  • ReDoc 文档: http://127.0.0.1:8000/redoc               ║
    ╚══════════════════════════════════════════════════════════╝
    """)
