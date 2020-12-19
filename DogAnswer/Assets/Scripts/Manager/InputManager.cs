using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using System.Text.RegularExpressions;

namespace DogAnswer
{
    public class InputManager: Utility.Singleton<InputManager>
    {
        public string SearchText = string.Empty;
        public InputField searchField;

        private const string SPLIT_CHARACTER = ",";

        public void ChangeSearchText()
        {
            SearchText = searchField.text;
        }

        public void Search()
        {
            var splitedTexts = Regex.Split(SearchText, SPLIT_CHARACTER);

            List<string> findTerms = new List<string>();
            List<string> ignoreTerms = new List<string>();

            // 찾을 텀, 무시할 텀 분리
            foreach (var splitedText in splitedTexts)
            {
                if (splitedText.StartsWith("!"))
                {
                    var text = splitedText.Replace("!", "");
                    ignoreTerms.Add(text);
                }
                else
                {
                    ignoreTerms.Add(splitedText);
                }
            }

            SearchManager.Instance.Search(findTerms, ignoreTerms);
        }
    }
}