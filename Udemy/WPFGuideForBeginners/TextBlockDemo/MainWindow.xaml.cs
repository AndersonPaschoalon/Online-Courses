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

namespace TextBlockDemo
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            this.myTextBlock.Text = "Hello from Code Behind!";
            this.myTextBlock.Foreground = Brushes.BlueViolet;

            // add textbloxk without xaml
            TextBlock runtimeTextBlock = new TextBlock();
            runtimeTextBlock.Text = "Runtime Hello World!";

            this.RuntimeStack.Children.Insert(0, runtimeTextBlock);

            runtimeTextBlock.Inlines.Add(
                new Run("Foi adicionado usando inlines")
                {
                    Foreground = Brushes.Red,
                    TextDecorations = TextDecorations.Underline,
                }
            );
            
            runtimeTextBlock.Foreground = Brushes.DeepSkyBlue;



        }

        private void Hyperlink_RequestNavigate(object sender, RequestNavigateEventArgs e)
        {
            System.Diagnostics.Process.Start(e.Uri.AbsoluteUri);
        }
    }
}
