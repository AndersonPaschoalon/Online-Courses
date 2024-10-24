using InstagramUserControlDemo.Models;
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
    /// Interação lógica para PicturePostUC.xam
    /// </summary>
    public partial class PicturePostUC : UserControl
    {
        public PicturePostUC(PicturePostModel picturePostModel)
        {
            InitializeComponent();
            ImageOfPost.Source = picturePostModel.PostImage;
        }

        private void PostImage_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            PostOps.ExecLikeOperation();
        }
    }
}
