﻿using CasaDoCodigo.Models;
using CasaDoCodigo.Repositories;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CasaDoCodigo.Controllers
{
    public class PedidoController : Controller
    {

        private readonly IProdutoRepository produtoRepository;

        private readonly IPedidoRepository pedidoRepository;

        public PedidoController(IProdutoRepository produtoRepository,
                                IPedidoRepository pedidoRepository)
        {
            this.produtoRepository = produtoRepository;
            this.pedidoRepository = pedidoRepository;
        }


        // /pedido/cadastro
        public IActionResult Cadastro()
        {
            return View();
        }

        // /pedido/carrinho
        public IActionResult Carrinho(string codigo)
        {
            if (!string.IsNullOrEmpty(codigo))
            {
                pedidoRepository.AddItem(codigo);
            }
            Pedido pedido = pedidoRepository.GetPedido();
            return View(pedido.Itens);
        }

        // /pedido/carrossel
        public IActionResult Carrossel()
        {
            return View(this.produtoRepository.GetProdutos());
        }

        // /pedido/resumo
        public IActionResult Resumo()
        {
            Pedido pedido = this.pedidoRepository.GetPedido();
            return View(pedido);
        }


    }
}
