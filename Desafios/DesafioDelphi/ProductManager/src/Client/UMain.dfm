object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Form1'
  ClientHeight = 456
  ClientWidth = 860
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  OnCreate = FormCreate
  DesignSize = (
    860
    456)
  TextHeight = 15
  object Refresh: TButton
    Left = 0
    Top = 8
    Width = 75
    Height = 25
    Caption = 'Refresh'
    TabOrder = 0
    OnClick = RefreshClick
  end
  object DBGrid1: TDBGrid
    Left = 0
    Top = 39
    Width = 852
    Height = 409
    Anchors = [akLeft, akTop, akRight, akBottom]
    DataSource = DataSource1
    TabOrder = 1
    TitleFont.Charset = DEFAULT_CHARSET
    TitleFont.Color = clWindowText
    TitleFont.Height = -12
    TitleFont.Name = 'Segoe UI'
    TitleFont.Style = []
  end
  object DBNavigator1: TDBNavigator
    Left = 612
    Top = 8
    Width = 240
    Height = 25
    DataSource = DataSource1
    TabOrder = 2
  end
  object FDMemTable1: TFDMemTable
    AfterOpen = FDMemTable1AfterOpen
    BeforePost = FDMemTable1BeforePost
    BeforeDelete = FDMemTable1BeforeDelete
    AfterRefresh = FDMemTable1AfterRefresh
    FetchOptions.AssignedValues = [evMode]
    FetchOptions.Mode = fmAll
    ResourceOptions.AssignedValues = [rvSilentMode]
    ResourceOptions.SilentMode = True
    UpdateOptions.AssignedValues = [uvCheckRequired, uvAutoCommitUpdates]
    UpdateOptions.CheckRequired = False
    UpdateOptions.AutoCommitUpdates = True
    Left = 136
    Top = 144
    object FDMemTable1id: TIntegerField
      FieldName = 'id'
    end
    object FDMemTable1Name: TStringField
      FieldName = 'Name'
    end
    object FDMemTable1Price: TCurrencyField
      FieldName = 'Price'
    end
    object FDMemTable1Description: TStringField
      FieldName = 'Description'
      Size = 50
    end
    object FDMemTable1Manufacturer: TStringField
      FieldName = 'Manufacturer'
    end
  end
  object DataSource1: TDataSource
    DataSet = FDMemTable1
    Left = 216
    Top = 144
  end
end
