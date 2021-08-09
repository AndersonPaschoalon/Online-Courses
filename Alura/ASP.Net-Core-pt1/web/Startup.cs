using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace web
{
    public class Startup
    {
        enum runMethod
        { 
            RUN,
            ENDPOINTS
        };

        enum serviceType
        {
            TRANSIENT,
            SCOPE,
            SINGLETON
        };

        const runMethod RUN = runMethod.RUN;
        const serviceType SERVICE = serviceType.TRANSIENT;


        // This method gets called by the runtime. Use this method to add services to the container.
        // For more information on how to configure your application, visit https://go.microsoft.com/fwlink/?LinkID=398940
        public void ConfigureServices(IServiceCollection services)
        {
            if (SERVICE == serviceType.TRANSIENT)
            {
                services.AddTransient<ICatalogo, Catalogo>();
                services.AddTransient<IRelatorio, Relatorio>();
            }
            else if (SERVICE == serviceType.SCOPE)
            {
                services.AddScoped<ICatalogo, Catalogo>();
                services.AddScoped<IRelatorio, Relatorio>();
            }
            else if (SERVICE == serviceType.SINGLETON)
            {

                var cat = new Catalogo();
                services.AddSingleton<ICatalogo>(cat);
                services.AddSingleton<IRelatorio>(new Relatorio(cat));

            }

        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env, IServiceProvider serviceProfiver)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            bool test01 = false;
            bool test02 = true;
            ICatalogo catalogo = serviceProfiver.GetService<ICatalogo>();
            IRelatorio relatorio = serviceProfiver.GetService<IRelatorio>();


            if (RUN == runMethod.ENDPOINTS)
            {
                app.UseRouting();
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/", async context =>
                    {
                        await relatorio.renderHtml(context);
                    });
                });
            }
            if (RUN == runMethod.RUN)
            {
                app.Run(async (context) =>
                {
                    await relatorio.renderHtml(context);
                });
            }

        }
    }
}
