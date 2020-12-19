using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace DogAnswer
{
    public class InputManager: Utility.Singleton<InputManager>
    {
        public string SearchText = string.Empty;
        public InputField searchField;

        public void ChangeSearchText()
        {
            SearchText = searchField.text;
        }

        public void Search()
        {
            Debug.LogError(SearchText);
        }
    }
}