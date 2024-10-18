using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace SliderDemo
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void mySlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {

            if (this.myTextBlock != null)
            {
                this.myTextBlock.Text = "Slider value is " + this.mySlider.Value.ToString();

                double fontSizeMod = 8 + 0.05 * this.mySlider.Value;

                this.myTextBlock.FontSize = fontSizeMod;
            }
        }
    }
}
