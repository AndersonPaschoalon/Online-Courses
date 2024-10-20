using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataBindingListToClass
{
    class Cars
    {
        public static List<Car> GetCars() 
        {
            return new List<Car>() {
                new Car(){ Owner="Mike", Type=CarType.Hatchback, BrandName=CarBrand.Hyundai},
                new Car(){ Owner="Ema", Type=CarType.Sedan, BrandName=CarBrand.Honda},
                new Car(){ Owner="Jon", Type=CarType.SUV, BrandName=CarBrand.VW},
            }.ToList();
        }
    }
}
