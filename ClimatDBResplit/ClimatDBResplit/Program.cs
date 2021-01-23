using System;
using System.IO;

namespace ClimatDBResplit
{
    class Program
    {
        static string fileName = "twitter_sentiment_data.csv";
        static string negativeFileName = "negative_twitter_sentiment_data.txt";
        static string positiveFileName = "positive_twitter_sentiment_data.txt";
        static string neutralFileName = "neutral_twitter_sentiment_data.txt";

        static void Main()
        {
            StreamWriter negative = File.CreateText(negativeFileName);
            StreamWriter positive = File.CreateText(positiveFileName);
            StreamWriter neutral = File.CreateText(neutralFileName);

            using (StreamReader reader = new StreamReader(fileName))
            {
                string line;
                reader.ReadLine();
                while ((line = reader.ReadLine()) != null)
                {
                    int status;
                    try
                    {
                        var statusString = line.Substring(0, line.IndexOf(","));

                        if (!Int32.TryParse(statusString, out status))
                            continue;
                    }
                    catch
                    {
                        continue;
                    }

                    string text;
                    try
                    {
                        text = line.Substring(line.IndexOf(",") + 1, line.LastIndexOf(",") - 2).Replace("\n", "").Replace("\"", "").Replace("RT", "").Replace("@", "").Replace("Ã¢â‚¬Â¦", "").Replace(" &amp;", "")
                            .Replace("Ã¢â‚¬Å“", "");
                        if (text.Contains("https://t.co"))
                            text = text.Remove(text.IndexOf("https://t.co"));
                        text.Trim();
                    }
                    catch
                    {
                        continue;
                    }

                    if (status > 0)
                        positive.WriteLine(text);
                    else if (status == 0)
                        neutral.WriteLine(text);
                    else
                        negative.WriteLine(text);
                }
            }

            negative.Close();
            positive.Close();
            neutral.Close();
        }
    }
}
