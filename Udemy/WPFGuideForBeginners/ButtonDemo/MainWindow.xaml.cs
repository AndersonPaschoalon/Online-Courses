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
//using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ButtonDemo
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

        private void myButton_Click(object sender, RoutedEventArgs e)
        {
            if (this.MyLabel.FontSize < 100)
            {
                this.MyLabel.FontSize++;
            }
            else
            {
                this.MyLabel.FontSize = 10;
            }

            if (this.MyLabel.Foreground == Brushes.Black)
            {
                this.MyLabel.Foreground = Brushes.Coral;
            }
            else
            {
                this.MyLabel.Foreground = Brushes.Black;
            }
                
        }

        private void myButton_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (this.MyLabel.FontSize > 10)
            {
                this.MyLabel.FontSize--;
            }
            else
            {
                this.MyLabel.FontSize = 10;
            }

            if (this.MyLabel.Foreground == Brushes.Black)
            {
                this.MyLabel.Foreground = Brushes.Purple;
            }
            else
            {
                this.MyLabel.Foreground = Brushes.Black;
            }
        }

        private void myButton_MouseEnter(object sender, MouseEventArgs e)
        {
            this.MyLabel.Foreground = Brushes.Magenta;
        }

        private void myButton_MouseLeave(object sender, MouseEventArgs e)
        {
            this.MyLabel.Foreground = Brushes.Black;
        }

        private void SkyrimSavePngExtractor(object sender, RoutedEventArgs e)
        {
            // Path to the Skyrim save file (.ess)
            string saveFilePath = "Save 874 - Kasin  Solitude  350.28.21.ess";


            SkyrimSaveExtractor.ExtractThumbnail(saveFilePath);

        }
    }
}
