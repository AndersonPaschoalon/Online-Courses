using System;
using Microsoft.EntityFrameworkCore.Storage;
using Microsoft.Extensions.Logging;

namespace Alura.Loja.Testes.ConsoleApp
{
    internal class NullLogger : ILogger
    {
        public IDisposable BeginScope<TState>(TState state)
        {
            return null;
        }

        public bool IsEnabled(LogLevel logLevel)
        {
            return true;
        }

        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception exception, Func<TState, Exception, string> formatter)
        {
            //não faz nada
        }
    }

    public class SqlLogger : ILogger
    {
        public SqlLogger()
        { 
        }

        public IDisposable BeginScope<TState>(TState state)
        {
            return null;
        }

        public bool IsEnabled(LogLevel logLevel)
        {
            return true;
        }

        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception exception, Func<TState, Exception, string> formatter)
        {
            Console.WriteLine("");
            Console.WriteLine(formatter(state, exception));
            Console.WriteLine("");
        }
    }

    internal class SqlLoggerProvider: ILoggerProvider
    {
        internal static ILoggerProvider Create()
        {
            return new SqlLoggerProvider();
        }

        public ILogger CreateLogger(string categoryName)
        {
            if (categoryName == typeof(IRelationalCommandBuilderFactory).FullName)
            {
                return new SqlLogger();
            }
            return new NullLogger();
        }

        public void Dispose()
        {
            throw new NotImplementedException();
        }
    }



}