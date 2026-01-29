unit Backend.Data.vo.v1.ProductVO;


interface

uses
  MVCFramework,
  MVCFramework.Commons,
  MVCFramework.Serializer.Commons;

type
  [MVCNameCase(ncCamelCase)]
  TProductVO = class
  private
    fId: Int64;
    fName: String;
    fPrice: Double;
    fDescription: String;
    fManufacturer: String;
    procedure SetId(const Value: Int64);
    procedure SetName(const Value: String);
    procedure SetPrice(const Value: Double);
    procedure SetDescription(const Value: String);
    procedure SetManufacturer(const Value: String);
  public
    property Id: Int64 read fId write fId;
    property Name: String read fName write fName;
    property Price: Double read fPrice write fPrice;
    property Description: String read fDescription write fDescription;
    property Manufacturer: String read fManufacturer write fManufacturer;
    // test
    function GetById(pId: Integer): TProductVO;


    constructor Create(Id: Int64; Name: String; Price: Double;
      Description: String; Manufacturer: String);
  end;

implementation

constructor TProductVO.Create(Id: Int64; Name: String; Price: Double; Description: String; Manufacturer: String);
begin
  inherited Create;
  fId := Id;
  fName := Name;
  fPrice := Price;
  fDescription := Description;
  fManufacturer := Manufacturer;
end;

procedure TProductVO.SetId(const Value: Int64);
begin
  fId := Value;
end;

procedure TProductVO.SetName(const Value: string);
begin
  fName := Value;
end;

procedure TProductVO.SetPrice(const Value: Double);
begin
  fPrice := Value;
end;

procedure TProductVO.SetDescription(const Value: string);
begin
  fDescription := Value
end;

procedure TProductVO.SetManufacturer(const Value: string);
begin
  fManufacturer := Value;
end;

function TProductVO.GetById(pId: Integer): TProductVO;
var
  lProduct: TProductVO;
begin
  lProduct := TProductVO.Create(pId, '', 0.0, '', '');
  lProduct.fId := pId;
  lProduct.fName := 'Product ';
  lProduct.fDescription := 'Product Description';
  lProduct.fPrice := 2.5 * pId;
  lProduct.fManufacturer := 'Product Manufacturer';

  Result := lProduct;
end;

end.

