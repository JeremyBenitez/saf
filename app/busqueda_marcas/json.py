datos = [{
  "filtro": "RP",
  "total_cantidad": 121668.0,
  "total_usd": 675291.7255999972,
  "valores_tiendas": {
    "BABILON": {
      "cantidad": 9220.0,
      "producto_mas_vendido": {
        "cantidad": 477.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 50010.35400000006
    },
    "BARALT": {
      "cantidad": 3796.0,
      "producto_mas_vendido": {
        "cantidad": 176.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 21205.152200000008
    },
    "CABIMAS": {
      "cantidad": 8993.0,
      "producto_mas_vendido": {
        "cantidad": 662.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 48179.280900000034
    },
    "CABUDARE": {
      "cantidad": 7380.0,
      "producto_mas_vendido": {
        "cantidad": 483.0,
        "codigo": "RPCA01800012",
        "nombre": "MEDIAS DE CABALLERO CORTAS"
      },
      "total_USD": 38103.859300000004
    },
    "CAGUA": {
      "cantidad": 8888.0,
      "producto_mas_vendido": {
        "cantidad": 392.0,
        "codigo": "RPCA01800012",
        "nombre": "MEDIAS DE CABALLERO CORTAS"
      },
      "total_USD": 48269.71530000005
    },
    "CATIA": {
      "cantidad": 8211.0,
      "producto_mas_vendido": {
        "cantidad": 460.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 49614.99909999997
    },
    "CRUZ VERDE": {
      "cantidad": 7448.0,
      "producto_mas_vendido": {
        "cantidad": 303.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 47488.17450000002
    },
    "GUACARA": {
      "cantidad": 6340.0,
      "producto_mas_vendido": {
        "cantidad": 642.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 39176.88970000007
    },
    "GUANARE": {
      "cantidad": 6732.0,
      "producto_mas_vendido": {
        "cantidad": 410.0,
        "codigo": "RPDA01800013",
        "nombre": "MEDIAS DE DAMA CORTAS"
      },
      "total_USD": 33933.266
    },
    "KAPITANA": {
      "cantidad": 10334.0,
      "producto_mas_vendido": {
        "cantidad": 647.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 63607.86480000004
    },
    "MATURIN": {
      "cantidad": 11573.0,
      "producto_mas_vendido": {
        "cantidad": 904.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 64715.395800000166
    },
    "PROPATRIA": {
      "cantidad": 8269.0,
      "producto_mas_vendido": {
        "cantidad": 352.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 45720.0303000001
    },
    "UPATA": {
      "cantidad": 9760.0,
      "producto_mas_vendido": {
        "cantidad": 513.0,
        "codigo": "RPUS13200001",
        "nombre": "ROPA SURTIDA SHEIN"
      },
      "total_USD": 44538.08670000006
    },
    "VALENCIA": {
      "cantidad": 9036.0,
      "producto_mas_vendido": {
        "cantidad": 712.0,
        "codigo": "RPNO00200038",
        "nombre": "FRANELA DE NINO 4"
      },
      "total_USD": 52322.88760000011
    },
    "VALERA": {
      "cantidad": 5688.0,
      "producto_mas_vendido": {
        "cantidad": 212.0,
        "codigo": "RPUS01800001",
        "nombre": "MEDIAS UNISEX LARGAS"
      },
      "total_USD": 28405.769400000005
    }
  }
}]





ordenado_por_cantidad = dict(sorted(datos[0]['valores_tiendas'].items(), key=lambda x: x[1]['cantidad'], reverse=True))
print(ordenado_por_cantidad)
  