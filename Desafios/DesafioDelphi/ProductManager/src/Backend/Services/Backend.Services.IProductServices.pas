unit Backend.Services.IProductServices;

interface

uses
  System.Generics.Collections,
  Backend.Data.vo.v1.ProductVO;

type
  IProductServices = interface
    ['{F8B48C83-B359-4814-BEAB-6B166FDEFAFD}']
    function GetById(pId: Integer): TProductVO;
    function GetAll(): TObjectList<TProductVO>;
    function CreateProduct(const AProductVo: TProductVO): Boolean;
    function UpdateProduct(const AProductVo: TProductVO): Boolean;
    function DeleteProduct(pId: Integer): Boolean;
  end;


implementation

end.

