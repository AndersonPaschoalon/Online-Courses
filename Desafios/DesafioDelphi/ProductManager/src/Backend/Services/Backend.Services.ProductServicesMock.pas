unit Backend.Services.ProductServicesMock;

interface

uses
  System.Generics.Collections,
  Backend.Services.IProductServices,
  Backend.Data.vo.v1.ProductVO;

type
  TProductServicesMock = class(TInterfacedObject, IProductServices)
  private
    FProductList: TObjectList<TProductVO>;
  public
    constructor Create;
    destructor Destroy; override;
    function GetById(pId: Integer): TProductVO;
    function GetAll(): TObjectList<TProductVO>;
    function CreateProduct(const AProductVo: TProductVO): Boolean;
    function UpdateProduct(const AProductVo: TProductVO): Boolean;
    function DeleteProduct(pId: Integer): Boolean;
  end;

implementation

{ TProductServicesMock }

constructor TProductServicesMock.Create;
begin
  inherited Create;
  FProductList := TObjectList<TProductVO>.Create(True);  // Automatically free the products when the list is freed

  // Add initial products to the list
  FProductList.Add(TProductVO.Create(1, 'Abacate', 1.0, 'Fruta', 'Fazenda Ametista'));
  FProductList.Add(TProductVO.Create(2, 'Banana', 1.0, 'Fruta', 'Fazenda Barranco'));
  FProductList.Add(TProductVO.Create(3, 'Carambola', 1.0, 'Fruta', 'Fazenda Cavalo'));
  FProductList.Add(TProductVO.Create(4, 'Damasco', 1.0, 'Fruta', 'Fazenda Da Avó'));
  FProductList.Add(TProductVO.Create(5, 'Espinafre', 1.0, 'Verdura', 'Fazenda Esmeralda'));
  FProductList.Add(TProductVO.Create(6, 'Goiaba', 1.0, 'Fruta', 'Fazenda Goiás'));
end;

destructor TProductServicesMock.Destroy;
begin
  FProductList.Free;  // Free the list of products
  inherited Destroy;
end;

function TProductServicesMock.GetById(pId: Integer): TProductVO;
var
  lProduct: TProductVO;
begin
  Result := nil;
  for lProduct in FProductList do
  begin
    if lProduct.ID = pId then
    begin
      Result := lProduct;
      Break;
    end;
  end;
end;

function TProductServicesMock.GetAll(): TObjectList<TProductVO>;
begin
  Result := FProductList;  // Return the current list of products
end;

function TProductServicesMock.CreateProduct(const AProductVo: TProductVO): Boolean;
begin
  // Add the new product to the list
  FProductList.Add(AProductVo);
  Result := True;  // Return success
end;

function TProductServicesMock.UpdateProduct(const AProductVo: TProductVO): Boolean;
var
  i: Integer;
  lProduct: TProductVO;
begin
  Result := False;
  for i := 0 to FProductList.Count - 1 do
  begin
    lProduct := FProductList[i];
    if lProduct.ID = AProductVo.Id then
    begin
      lProduct.Name := AProductVo.Name;
      lProduct.Price := AProductVo.Price;
      lProduct.Description := AProductVo.Description;
      lProduct.Manufacturer := AProductVo.Manufacturer;
      Result := True;
      Break;
    end;
  end;
end;

function TProductServicesMock.DeleteProduct(pId: Integer): Boolean;
var
  i: Integer;
begin
  Result := False;
  for i := 0 to FProductList.Count - 1 do
  begin
    if FProductList[i].ID = pId then
    begin
      FProductList.Delete(i);
      Result := True;
      Break;
    end;
  end;
end;

end.


