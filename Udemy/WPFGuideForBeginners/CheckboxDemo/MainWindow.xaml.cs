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

namespace CheckboxDemo
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

        private void CbParentCheckedChanged(object sender, RoutedEventArgs e)
        {
            bool newVal = (cbParent.IsChecked == true);
            cbCheese.IsChecked = newVal;
            cbHam.IsChecked = newVal;
            cbTuna.IsChecked = newVal;
            cbPeperoni.IsChecked = newVal;
        }

        private void CbToppingsCheckedChange(object sender, RoutedEventArgs e)
        {
            cbParent.IsChecked = null;
            if ((cbCheese.IsChecked == true) && (cbTuna.IsChecked == true) && (cbHam.IsChecked == true) && (cbHam.IsChecked == true) && (cbPeperoni.IsChecked == true))
            {
                cbParent.IsChecked = true;
            }
            else if ((cbCheese.IsChecked == false) && (cbTuna.IsChecked == false) && (cbHam.IsChecked == false) && (cbHam.IsChecked == false) && (cbPeperoni.IsChecked == false))
            {
                cbParent.IsChecked = false;
            }
        }

    }
}
