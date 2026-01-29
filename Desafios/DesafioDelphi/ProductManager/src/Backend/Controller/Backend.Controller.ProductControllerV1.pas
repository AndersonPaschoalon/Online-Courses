unit Backend.Controller.ProductControllerV1;

interface

uses
  MVCFramework,
  MVCFramework.Commons,
  MVCFramework.Serializer.Commons,
  MVCFramework.Serializer.JsonDataObjects,
  System.Generics.Collections,
  Backend.Services.ProductServices,
  Backend.Services.ProductServicesMock,
  Backend.Services.IProductServices,
  Backend.Data.vo.v1.ProductVO;


type


  [MVCPath('/api/v1')]
  TProductManagerController = class(TMVCController)

  private
    FProductServices: IProductServices;

  protected
    procedure OnBeforeAction(Context: TWebContext; const AActionName: string; var Handled: Boolean); override;
    procedure OnAfterAction(Context: TWebContext; const AActionName: string); override;

  public
    constructor Create; override;
    destructor Destroy; override;


    {Test endpoint: just print Hello DelphiMVCFramework World}
    [MVCPath]
    [MVCHTTPMethod([httpGET])]
    procedure Index;

    {This endpoints confirms the service is indeed active}
    [MVCPath('/isactive')]
    [MVCHTTPMethod([httpGET])]
    [MVCProduces(TMVCMediaType.APPLICATION_JSON)]
    procedure GetIsActive();

    [MVCPath('/products')]
    [MVCHTTPMethod([httpGET])]
    function GetAllProducts: TObjectList<TProductVO>;

    [MVCPath('/product/($ID)')]
    [MVCHTTPMethod([httpGET])]
    function GetProduct(ID: Integer): TProductVO;

    [MVCPath('/create')]
    [MVCHTTPMethod([httpPOST])]
    procedure CreateProduct;

    [MVCPath('/update/($ID)')]
    [MVCHTTPMethod([httpPUT])]
    procedure UpdateProduct(ID: Integer);

    [MVCPath('/delete/($ID)')]
    [MVCHTTPMethod([httpDELETE])]
    procedure DeleteProduct(ID: Integer);


  end;

implementation

uses
  FireDAC.Comp.Client,
  FireDAC.Stan.Intf,
  FireDAC.Stan.Option,
  FireDAC.Stan.Error,
  FireDAC.UI.Intf,
  FireDAC.Phys.Intf,
  FireDAC.Stan.Def,
  FireDAC.Stan.Pool,
  FireDAC.Stan.Async,
  FireDAC.Phys,
  FireDAC.Phys.PG,
  FireDAC.Phys.PGDef,
  FireDAC.VCLUI.Wait,
  FireDAC.Stan.Param,
  FireDAC.DatS,
  FireDAC.DApt.Intf,
  FireDAC.DApt,
  System.SysUtils,
  MVCFramework.Logger;

constructor TProductManagerController.Create;
begin
  inherited;

  //FProductServices := TProductServicesMock.Create();
  FProductServices := TProductServices.Create;
end;

destructor TProductManagerController.Destroy;
begin
  // Free ProductServices when the controller is destroyed
  inherited;
end;

procedure TProductManagerController.Index;
begin
  //use Context property to access to the HTTP request and response 
  Render('Hello DelphiMVCFramework World');
end;

procedure TProductManagerController.GetIsActive();
begin
  Render('True');
end;

procedure TProductManagerController.OnAfterAction(Context: TWebContext; const AActionName: string); 
begin
  { Executed after each action }
  inherited;
end;

procedure TProductManagerController.OnBeforeAction(Context: TWebContext; const AActionName: string; var Handled: Boolean);
begin
  { Executed before each action
    if handled is true (or an exception is raised) the actual
    action will not be called }
  inherited;
end;

function TProductManagerController.GetAllProducts(): TObjectList<TProductVO>;
begin
  Result := FProductServices.GetAll();
end;

function TProductManagerController.GetProduct(ID: Integer): TProductVO;
begin
  Result := FProductServices.GetById(ID);
end;


procedure TProductManagerController.CreateProduct;
var
  lProduct: TProductVO;
begin
  lProduct := Context.Request.BodyAs<TProductVO>;

  try
    if FProductServices.CreateProduct(lProduct) then
      begin
        Render(HTTP_STATUS.Created, 'Product Created')
      end
    else
      begin
        Render(HTTP_STATUS.InternalServerError, 'Internal Server Error');
      end;

  finally

  end;
end;


procedure TProductManagerController.UpdateProduct(ID: Integer);
var
  lProduct: TProductVO;
begin
  lProduct := Context.Request.BodyAs<TProductVO>;
  lProduct.Id := ID;

  try
    if FProductServices.UpdateProduct(lProduct) then
      begin
        Render(HTTP_STATUS.OK, 'OK')
      end
    else
      begin
        Render(HTTP_STATUS.InternalServerError, 'Internal Server Error');
      end;

  finally

  end;
end;


procedure TProductManagerController.DeleteProduct(ID: Integer);
begin
  try
    if FProductServices.DeleteProduct(ID) then
      begin
        Render(HTTP_STATUS.OK, 'OK')
      end
    else
      begin
        Render(HTTP_STATUS.InternalServerError, 'Internal Server Error');
      end;

  finally

  end;
end;


end.
