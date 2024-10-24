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

namespace InstagramUserControlDemo.UserControls
{
    /// <summary>
    /// Interação lógica para PostOperationsUC.xam
    /// </summary>
    public partial class PostOperationsUC : UserControl
    {
        private bool PostLike { get; set; }


        public PostOperationsUC()
        {
            InitializeComponent();
            PostLike = false;
        }

        private void LikePost() 
        {
            Heart.Source = new BitmapImage(new Uri(@"\Icons\like.png", UriKind.RelativeOrAbsolute));
            PostLike = true;

        }

        private void UnlikePost()
        {
            Heart.Source = new BitmapImage(new Uri(@"\Icons\nolike.png", UriKind.Relative));
            PostLike = false;

        }

        public void ExecLikeOperation()
        {
            if (!PostLike)
            {
                LikePost();
            }
            else
            {
                UnlikePost();
            }
        }


        private void Heart_MouseDown(object sender, MouseButtonEventArgs e)
        {
            ExecLikeOperation();
        }

        private void Comment_MouseDown(object sender, MouseButtonEventArgs e)
        {

        }

        private void Send_MouseDown(object sender, MouseButtonEventArgs e)
        {

        }
    }
}
