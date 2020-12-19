using System.Collections.Generic;
using System.Collections;
using UnityEngine;

namespace DogAnswer
{
    public class SearchManager : Utility.Singleton<SearchManager>
    {
        // 검색한 사진 이름 return
        public List<string> Search(List<string> findTerms, List<string> ignoreTerms, out string dogName)
        {
            var dogNames = TableManager.Instance.DogNames;


            // 개 이름이 있는지 검사.
            dogName = string.Empty;
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
                return null;
            }

            findTerms.Remove(dogName);

            VectorTable vectorTable = TableManager.Instance.vectorTables[dogName];

            List<int> DogPhotoIndexs = new List<int>();

            // 찾는 검색어가 없다면 해당 개 사진 다 출력
            if (findTerms.Count == 0)
            {
                for (int i = 0; i < vectorTable.Columns.Count; i++)
                {
                    DogPhotoIndexs.Add(i);
                }
            }

            // 검색할 사진의 개 사진 인덱스 추가
            foreach (var term in findTerms)
            {


                if (vectorTable.RowTable.TryGetValue(term, out List<float> values))
                {
                    for (int i = 0; i < values.Count; i++)
                    {
                        if (values[i] > 0)
                        {
                            if (!DogPhotoIndexs.Contains(i))
                            {
                                DogPhotoIndexs.Add(i);
                            }
                        }
                    }
                }
            }

            // 무시할 검색어 포함한 사진 인덱스 제거
            foreach (var term in ignoreTerms)
            {
                if (vectorTable.RowTable.TryGetValue(term, out List<float> values))
                {
                    for (int i = 0; i < values.Count; i++)
                    {
                        if (values[i] > 0)
                        {
                            if (DogPhotoIndexs.Contains(i))
                            {
                                DogPhotoIndexs.Remove(i);
                            }
                        }
                    }
                }
            }

            List<string> result = new List<string>();

            foreach (var index in DogPhotoIndexs)
            {
                string photoName = vectorTable.Columns[index];

                result.Add(photoName);
            }

            return result;
        }
    }
}