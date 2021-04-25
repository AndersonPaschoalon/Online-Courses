using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using CasaDoCodigo.Models;
using CasaDoCodigo.Repositories;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace CasaDoCodigo
{
    public class Startup
    {
        public enum DB_CREATION
        {
            USE_MIGRATIONS,
            APPLICATION_CONTEXT,
            DATA_SERVICE
        }

        private readonly DB_CREATION db_usage = DB_CREATION.DATA_SERVICE;

        public Startup(IConfiguration configuration)
        {

            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc();

            // -- sessao
            services.AddDistributedMemoryCache();
            services.AddSession();

            // -- configura DB service 
            string connectionString = Configuration.GetConnectionString("Default");
            services.AddDbContext<ApplicationContext>(options => options.UseSqlServer(connectionString));

            // -- register DataService class
            services.AddTransient<IDataService, DataService>();

            // register repository class
            services.AddTransient<IProdutoRepository, ProdutoRepository>();

            // pedido repository class
            services.AddTransient<IPedidoRepository, PedidoRepository>();

            // cadastro repository class
            services.AddTransient<ICadastroRepository, CadastroRepository>();

            // itemPedido repository class
            services.AddTransient<IItemPedidoRepository, ItemPedidoRepository>();

        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env, IServiceProvider serviceProvider)
        {
            if (env.IsDevelopment())
            {
                app.UseBrowserLink();
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Home/Error");
            }

            app.UseStaticFiles();
            app.UseSession();

            app.UseMvc(routes =>
            {
                routes.MapRoute(
                    name: "default",
                    template: "{controller=Pedido}/{action=Carrossel}/{codigo?}");
            });

            switch (this.db_usage)
            {
                case DB_CREATION.USE_MIGRATIONS:
                    {
                        serviceProvider.GetService<ApplicationContext>().Database.Migrate();
                        break;
                    }
                case DB_CREATION.APPLICATION_CONTEXT:
                    {
                        serviceProvider.GetService<ApplicationContext>().Database.EnsureCreated();
                        break;
                    }
                case DB_CREATION.DATA_SERVICE:
                    {
                        //serviceProvider.GetService<DataService>().InitializeDB();
                        serviceProvider.GetService<IDataService>().InitializeDB();
                        break;
                    }
                default:
                    {
                        serviceProvider.GetService<ApplicationContext>().Database.EnsureCreated();
                        break;
                    }
                
            }

            
        }
    }
}
