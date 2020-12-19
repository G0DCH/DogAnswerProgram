using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using System.Text.RegularExpressions;

namespace DogAnswer
{
    public class InputManager : Utility.Singleton<InputManager>
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
                if (splitedText == string.Empty)
                    continue;

                var trimmedText = splitedText.Trim(' ');

                if (trimmedText.StartsWith("!"))
                {
                    var text = trimmedText.Replace("!", "");
                    ignoreTerms.Add(ToUpperText(text));
                }
                else
                {
                    findTerms.Add(ToUpperText(trimmedText));
                }
            }

            var searchResults = SearchManager.Instance.Search(findTerms, ignoreTerms, out string dogName);

            // 검색 결과 이미지 출력
            if (searchResults != null && searchResults.Count > 0)
            {
                UIManager.Instance.ShowImages(dogName, searchResults);
            }
        }

        // 첫글자 혹은 공백 뒤 첫 글자 대문자로 변경
        private string ToUpperText(string text)
        {
            var splitedTexts = text.Split(' ');
            string resultText = string.Empty;

            foreach (var splitedText in splitedTexts)
            {
                var newText = char.ToUpper(splitedText[0]) + splitedText.Substring(1);
                resultText = resultText + newText + " ";
            }

            return resultText.Trim(' ');
        }
    }
}