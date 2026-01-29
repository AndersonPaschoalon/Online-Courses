unit UMain;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls, MVCFramework.RESTClient,
  Data.DB, FireDAC.Stan.Intf, FireDAC.Stan.Option, FireDAC.Stan.Param,
  FireDAC.Stan.Error, FireDAC.DatS, FireDAC.Phys.Intf, FireDAC.DApt.Intf,
  FireDAC.Comp.DataSet, FireDAC.Comp.Client, Vcl.Grids, Vcl.DBGrids,
  MVCFramework.DataSet.Utils, Vcl.ExtCtrls, Vcl.Buttons, Vcl.DBCtrls;

type
  TForm1 = class(TForm)
    Refresh: TButton;
    DBGrid1: TDBGrid;
    FDMemTable1: TFDMemTable;
    DataSource1: TDataSource;
    FDMemTable1id: TIntegerField;
    FDMemTable1Name: TStringField;
    FDMemTable1Price: TCurrencyField;
    FDMemTable1Description: TStringField;
    FDMemTable1Manufacturer: TStringField;
    DBNavigator1: TDBNavigator;
    procedure RefreshClick(Sender: TObject);
    procedure FDMemTable1AfterOpen(DataSet: TDataSet);
    procedure FDMemTable1BeforePost(DataSet: TDataSet);
    procedure FormCreate(Sender: TObject);
    procedure FDMemTable1BeforeDelete(DataSet: TDataSet);
    procedure FDMemTable1AfterRefresh(DataSet: TDataSet);
  private
    { Private declarations }
    FLoading: Boolean;
    procedure FRefreshDatabase();
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.dfm}

procedure TForm1.FDMemTable1AfterOpen(DataSet: TDataSet);
var
  lResponse: IRESTResponse;
  lRESTClient: MVCFramework.RESTClient.TRESTClient;

begin
  lRESTClient := MVCFramework.RESTClient.TRESTClient.Create('localhost', 8081);
  try
    lResponse := lRESTClient.doGET('/api/v1/products', []);

    FLoading := True;
    FDMemTable1.LoadFromJSONArrayString(lResponse.BodyAsString);
    FLoading := False;
  finally
    lRESTClient.Free;
  end;


end;

procedure TForm1.FDMemTable1AfterRefresh(DataSet: TDataSet);
begin
  FRefreshDatabase();
end;

procedure TForm1.FDMemTable1BeforeDelete(DataSet: TDataSet);
var
  lResponse: IRESTResponse;
  lRESTClient: MVCFramework.RESTClient.TRESTClient;
begin
  if FLoading then
  begin
    Exit
  end;

  lRESTClient := MVCFramework.RESTClient.TRESTClient.Create('localhost', 8081);

  try
    lResponse := lRESTClient.DataSetDelete('/api/v1/delete', FDMemTable1id.AsString);
  finally
    lRESTClient.Free;
  end;

end;

procedure TForm1.FDMemTable1BeforePost(DataSet: TDataSet);
var
  lResponse: IRESTResponse;
  lRESTClient: MVCFramework.RESTClient.TRESTClient;
begin
  if FLoading then
  begin
    Exit
  end;

  lRESTClient := MVCFramework.RESTClient.TRESTClient.Create('localhost', 8081);

  try
    if FDMemTable1.State = dsInsert then
      begin
        lResponse := lRESTClient.DataSetInsert('/api/v1/create', FDMemTable1);
      end
    else if FDMemTable1.State = dsEdit then
      begin
        lResponse := lRESTClient.DataSetUpdate('/api/v1/update', FDMemTable1, FDMemTable1id.AsString);
      end;
  finally
    lRESTClient.Free;
    FRefreshDatabase();
  end;

end;

procedure TForm1.FormCreate(Sender: TObject);
begin
   FLoading := False;
   FRefreshDatabase();
end;

procedure TForm1.RefreshClick(Sender: TObject);
begin
  FRefreshDatabase();
end;

procedure TForm1.FRefreshDatabase();
begin
  FDMemTable1.Close;
  FDMemTable1.Open;
end;

end.