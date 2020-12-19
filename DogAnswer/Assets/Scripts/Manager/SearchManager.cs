using System.Collections.Generic;
using System.Collections;
using UnityEngine;

namespace DogAnswer
{
    public class SearchManager: Utility.Singleton<SearchManager>
    {
        [SerializeField]
        private GameObject ImagePrefab;
        [SerializeField]
        private Transform Container;

        public void Search(List<string> containTexts, List<string> ignoreTexts)
        {

        }
    }
}