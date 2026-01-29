unit Backend.Services.ProductServices;

interface

uses
  System.SysUtils,
  System.Generics.Collections,
  FireDAC.Comp.Client,
  FireDAC.Stan.Param,
  Data.DB,
  Backend.Model.ProductRepository,
  Backend.Services.IProductServices,
  Backend.Data.vo.v1.ProductVO,
  Backend.Model.Product;

type
  TProductServices = class(TInterfacedObject, IProductServices)
  private
    fProductRepo: TProductRepository;
    class function ConvertToVO(const AProduct: TProduct): TProductVO;
    class function ConvertToProd(const AProductVo: TProductVO): TProduct;
  public
    constructor Create();

    function GetAll: TObjectList<TProductVO>;
    function GetById(pId: Integer): TProductVO;
    function CreateProduct(const AProductVo: TProductVO): Boolean;
    function UpdateProduct(const AProductVo: TProductVO): Boolean;
    function DeleteProduct(pId: Integer): Boolean;
  end;


implementation

class function TProductServices.ConvertToVO(const AProduct: TProduct): TProductVO;
begin
  Result := TProductVO.Create(
    AProduct.Id,
    AProduct.Name,
    AProduct.Price,
    AProduct.Description,
    AProduct.Manufacturer
  );
end;

class function TProductServices.ConvertToProd(const AProductVo: TProductVO): TProduct;
var
  lProd: TProduct;
begin
  lProd := TProduct.Create();
  lProd.Id := AProductVo.Id;
  lProd.Name := AProductVo.Name;
  lProd.Price := AProductVo.Price;
  lProd.Description := AProductVo.Description;
  lProd.Manufacturer := AProductVo.Manufacturer;

  Result := lProd;
end;

constructor TProductServices.Create();
begin
   fProductRepo := TProductRepository.Create;
end;

function TProductServices.GetAll: TObjectList<TProductVO>;
var
  lListProd: TObjectList<TProduct>;
  lProduct: TProduct;
  lProductVO: TProductVO;
  i: Integer;
begin
  Result := TObjectList<TProductVO>.Create(True);
  lListProd := fProductRepo.GetAll;
  try
    for i := 0 to lListProd.Count - 1 do
    begin
      lProduct := lListProd[i];
      lProductVO := ConvertToVO(lProduct);
      Result.Add(lProductVO);
    end;
  finally
    lListProd.Free;
  end;
end;

function TProductServices.GetById(pId: Integer): TProductVO;
var
  lProduct: TProduct;
  lProductVO: TProductVO;
begin
  lProduct := nil;
  lProductVO := nil;
  try
    lProduct :=  fProductRepo.GetById(pId);
    lProductVO := ConvertToVO(lProduct);
  finally
    Result := lProductVO;
  end;
end;

function TProductServices.CreateProduct(const AProductVo: TProductVO): Boolean;
var
  lProduct: TProductVO;
  lRet: Boolean;
begin
  lRet := False;
  try
    lRet := fProductRepo.CreateProduct(TProductServices.ConvertToProd(AProductVo));
  finally
    Result :=  lRet;
  end;
end;

function TProductServices.UpdateProduct(const AProductVo: TProductVO): Boolean;
var
  lProduct: TProductVO;
  lRet: Boolean;
begin
  lRet := False;
  try
    lRet := fProductRepo.UpdateProduct(TProductServices.ConvertToProd(AProductVo));
  finally
    Result :=  lRet;
  end;
end;

function TProductServices.DeleteProduct(pId: Integer): Boolean;
var
  lProduct: TProductVO;
  lRet: Boolean;
begin
  lRet := False;
  try
    lRet := fProductRepo.DeleteProduct(pId);
  finally
    Result :=  lRet;
  end;
end;


end.
