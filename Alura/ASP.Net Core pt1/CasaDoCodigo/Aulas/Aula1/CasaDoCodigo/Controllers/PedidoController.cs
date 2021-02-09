using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CasaDoCodigo.Controllers
{
    public class PedidoController : Controller
    {
        // /pedido/cadastro
        public IActionResult Cadastro()
        {
            return View();
        }

        // /pedido/carrinho
        public IActionResult Carrinho()
        {
            return View();
        }

        // /pedido/carrossel
        public IActionResult Carrossel()
        {
            return View();
        }

        // /pedido/resumo
        public IActionResult Resumo()
        {
            return View();
        }
    }
}
