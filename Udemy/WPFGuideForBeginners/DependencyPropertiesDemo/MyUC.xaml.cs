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

namespace DependencyPropertiesDemo
{
    /// <summary>
    /// Interação lógica para MyUC.xam
    /// </summary>
    public partial class MyUC : UserControl
    {



        public int Awsomeness
        {
            get { return (int)GetValue(AwsomenessProperty); }
            set { SetValue(AwsomenessProperty, value); }
        }

        // Using a DependencyProperty as the backing store for Awsomeness.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty AwsomenessProperty =
            DependencyProperty.Register("Awsomeness", typeof(int), typeof(MyUC), new PropertyMetadata(0));



        public MyUC()
        {
            InitializeComponent();
        }
    }
}
