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

namespace ContextMenuDemo
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


        private void miBold_Checked(object sender, RoutedEventArgs e)
        {
            this.myTB.FontWeight = FontWeights.Bold;
        }

        private void miItalic_Unchecked(object sender, RoutedEventArgs e)
        {
            this.myTB.FontStyle = FontStyles.Normal;
        }

        private void miBold_Unchecked(object sender, RoutedEventArgs e)
        {
            this.myTB.FontWeight = FontWeights.Normal;
        }

        private void miItalic_Checked(object sender, RoutedEventArgs e)
        {
            this.myTB.FontStyle = FontStyles.Italic;
        }
    }
}
