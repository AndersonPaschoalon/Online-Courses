﻿using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;

namespace web
{
    public interface IRelatorio
    {
        Task renderHtml(HttpContext context);
    }
}