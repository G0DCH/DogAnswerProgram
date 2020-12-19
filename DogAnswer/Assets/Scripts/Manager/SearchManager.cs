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

        public void Search(List<string> findTerms, List<string> ignoreTerms)
        {
            var dogNames = TableManager.Instance.DogNames;


            // 개 이름이 있는지 검사.
            string dogName = string.Empty;
            foreach (var term in findTerms)
            {
                if (dogNames.Contains(term))
                {
                    dogName = term;
                    break;
                }
            }

            if (dogName == string.Empty)
            {
                UIManager.Instance.Alert("경고!! 개 이름을 입력해주세요!!!");
                return;
            }

            findTerms.Remove(dogName);
        }
    }
}