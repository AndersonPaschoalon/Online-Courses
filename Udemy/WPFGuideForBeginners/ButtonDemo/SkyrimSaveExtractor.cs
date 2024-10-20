using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System;
using System.Drawing;
using System.IO;
using System.Text;
using System.Drawing.Imaging;

namespace ButtonDemo
{
    public  class SkyrimSaveExtractor
    {
        public static void ExtractThumbnail(string filePath)
        {
            byte[] saveFileData = File.ReadAllBytes(filePath);
            Console.WriteLine($"File size: {saveFileData.Length} bytes");

            using (MemoryStream memoryStream = new MemoryStream(saveFileData))
            using (BinaryReader reader = new BinaryReader(memoryStream, Encoding.UTF8))
            {
                // Read and validate the magic header
                string magic = new string(reader.ReadChars(13));
                if (magic != "TESV_SAVEGAME")
                {
                    Console.WriteLine("Invalid save file format.");
                    return;
                }

                // Read the header size
                uint headerSize = reader.ReadUInt32();
                Console.WriteLine($"Header size: {headerSize}");

                // Skip the header data until we reach the screenshot size info
                reader.BaseStream.Seek(18, SeekOrigin.Current); // Skip version, save number, etc.
                string playerName = ReadWString(reader);
                uint playerLevel = reader.ReadUInt32();
                string playerLocation = ReadWString(reader);
                string gameDate = ReadWString(reader);
                string playerRaceEditorId = ReadWString(reader);
                ushort playerSex = reader.ReadUInt16();
                float playerCurExp = reader.ReadSingle();
                float playerLvlUpExp = reader.ReadSingle();
                long fileTime = reader.ReadInt64();

                // Read screenshot width and height
                uint shotWidth = reader.ReadUInt32();
                uint shotHeight = reader.ReadUInt32();
                Console.WriteLine($"Screenshot dimensions: {shotWidth}x{shotHeight}");

                // Calculate the size of the screenshot data
                int screenshotDataSize = (int)(3 * shotWidth * shotHeight);
                Console.WriteLine($"Expected screenshot data size: {screenshotDataSize} bytes");

                // Read the screenshot data (RGB format)
                byte[] screenshotData = reader.ReadBytes(screenshotDataSize);
                if (screenshotData.Length != screenshotDataSize)
                {
                    Console.WriteLine("Failed to read the entire screenshot data.");
                    return;
                }

                // Convert the screenshot data to a bitmap
                Bitmap screenshot = new Bitmap((int)shotWidth, (int)shotHeight, PixelFormat.Format24bppRgb);
                int dataIndex = 0;

                for (int y = 0; y < shotHeight; y++)
                {
                    for (int x = 0; x < shotWidth; x++)
                    {
                        byte r = screenshotData[dataIndex++];
                        byte g = screenshotData[dataIndex++];
                        byte b = screenshotData[dataIndex++];
                        Color pixelColor = Color.FromArgb(r, g, b);
                        screenshot.SetPixel(x, (int)shotHeight - y - 1, pixelColor); // Flip Y-axis
                    }
                }

                // Save the screenshot as a PNG file
                string outputFilePath = Path.Combine(Path.GetDirectoryName(filePath), "screenshot.png");
                screenshot.Save(outputFilePath, ImageFormat.Png);
                Console.WriteLine($"Screenshot saved successfully to {outputFilePath}");
            }
        }

        // Helper method to read a null-terminated wide string (wstring)
        static string ReadWString(BinaryReader reader)
        {
            StringBuilder sb = new StringBuilder();
            while (true)
            {
                char c = reader.ReadChar();
                if (c == '\0') break;
                sb.Append(c);
            }
            return sb.ToString();
        }

    }
}
