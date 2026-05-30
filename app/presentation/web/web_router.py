from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.infraestructure.database import get_session
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.transaction_service import ListTransactionUseCase, GetTransactionUseCase
from app.application.services.category_service import ListCategoryUseCase
from app.application.services.account_service import ListAccountUseCase
from app.presentation.api.dependencies import get_current_user_from_cookie

router = APIRouter(tags=["web"])

templates = Jinja2Templates(directory="app/presentation/web/templates")

@router.get("/", response_class=HTMLResponse)
async def render_home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

@router.get("/login-page", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.get("/register-page", response_class=HTMLResponse)
async def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@router.get("/transaction-page", response_class=HTMLResponse)
async def render_transaction_page(
    request: Request, 
    current_user=Depends(get_current_user_from_cookie),
    session=Depends(get_session)
):
    if current_user is None:
        redirect_response = RedirectResponse(url="/login-page", status_code=303)
        redirect_response.delete_cookie("access_token")
        return redirect_response
        
    uow = UnitOfWork(session)
    service = ListTransactionUseCase(uow=uow)
    transactions = service.execute(offset=0, limit=100, current_user=current_user)
    
    return templates.TemplateResponse(
        request=request, 
        name="transaction.html",
        context={"transactions": transactions, "current_user": current_user}
    )

@router.get("/add-transaction-page", response_class=HTMLResponse)
async def render_add_transaction_page(
    request: Request, 
    current_user=Depends(get_current_user_from_cookie),
    session=Depends(get_session)
):
    if current_user is None:
        redirect_response = RedirectResponse(url="/login-page", status_code=303)
        redirect_response.delete_cookie("access_token")
        return redirect_response
        
    uow = UnitOfWork(session)
    category_service = ListCategoryUseCase(uow=uow)
    account_service = ListAccountUseCase(uow=uow)
    
    categories = category_service.execute(offset=0, limit=100, current_user=current_user)
    accounts = account_service.execute(offset=0, limit=100, current_user=current_user)
    
    return templates.TemplateResponse(
        request=request, 
        name="add-transaction.html",
        context={"categories": categories, "accounts": accounts, "current_user": current_user}
    )

@router.get("/edit-transaction-page/{id}", response_class=HTMLResponse)
async def render_edit_transaction_page(
    id: int,
    request: Request, 
    current_user=Depends(get_current_user_from_cookie),
    session=Depends(get_session)
):
    if current_user is None:
        redirect_response = RedirectResponse(url="/login-page", status_code=303)
        redirect_response.delete_cookie("access_token")
        return redirect_response
        
    uow = UnitOfWork(session)
    transaction_service = GetTransactionUseCase(uow=uow)
    category_service = ListCategoryUseCase(uow=uow)
    account_service = ListAccountUseCase(uow=uow)
    
    transaction = transaction_service.execute(id, current_user=current_user)
    categories = category_service.execute(offset=0, limit=100, current_user=current_user)
    accounts = account_service.execute(offset=0, limit=100, current_user=current_user)
    
    return templates.TemplateResponse(
        request=request, 
        name="edit-transaction.html",
        context={"transaction": transaction, "categories": categories, "accounts": accounts, "current_user": current_user}
    )

