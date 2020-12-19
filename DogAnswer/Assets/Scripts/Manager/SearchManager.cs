using System.Collections.Generic;
using System;

namespace DogAnswer
{
    public class IndexWeightSet : IComparable<IndexWeightSet>, IEquatable<IndexWeightSet>
    {
        public int index;
        public float weight;

        public IndexWeightSet(int myIndex, float myWeight)
        {
            index = myIndex;
            weight = myWeight;
        }

        public int CompareTo(IndexWeightSet other)
        {
            if (other == null)
            {
                return 1;
            }
            else
            {
                return weight.CompareTo(other.weight);
            }
        }

        public bool Equals(IndexWeightSet other)
        {
            if (other == null)
            {
                return false;
            }
            else
            {
                return weight.Equals(other.weight);
            }
        }
    }

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

            List<int> dogPhotoIndexes = new List<int>();
            List<IndexWeightSet> dogIndexWeightSets = new List<IndexWeightSet>();

            // 찾는 검색어가 없다면 해당 개 사진 다 출력
            if (findTerms.Count == 0)
            {
                for (int i = 0; i < vectorTable.Columns.Count; i++)
                {
                    dogPhotoIndexes.Add(i);
                }
            }

            // 검색할 사진의 개 사진 인덱스 추가
            foreach (var term in findTerms)
            {
                if (vectorTable.ColumnTable.TryGetValue(term, out List<float> values))
                {
                    for (int i = 0; i < values.Count; i++)
                    {
                        if (values[i] > 0)
                        {
                            if (!dogPhotoIndexes.Contains(i))
                            {
                                dogIndexWeightSets.Add(new IndexWeightSet(i, values[i]));
                                dogPhotoIndexes.Add(i);
                            }
                            else
                            {
                                // 가중치 더함.
                                dogIndexWeightSets[dogPhotoIndexes.IndexOf(i)].weight += values[i];
                            }
                        }
                    }
                }
            }

            // 무시할 검색어 포함한 사진 인덱스 제거
            foreach (var term in ignoreTerms)
            {
                if (vectorTable.ColumnTable.TryGetValue(term, out List<float> values))
                {
                    for (int i = 0; i < values.Count; i++)
                    {
                        if (values[i] > 0)
                        {
                            if (dogPhotoIndexes.Contains(i))
                            {
                                dogIndexWeightSets.RemoveAt(dogPhotoIndexes.IndexOf(i));
                                dogPhotoIndexes.Remove(i);
                            }
                        }
                    }
                }
            }

            // 내림차순 정렬
            dogIndexWeightSets.Sort();
            dogIndexWeightSets.Reverse();

            List<string> result = new List<string>();

            if (dogIndexWeightSets.Count > 0)
            {
                foreach (var set in dogIndexWeightSets)
                {
                    string photoName = vectorTable.Columns[set.index];
                    result.Add(photoName);
                }
            }
            else
            {
                foreach (var index in dogPhotoIndexes)
                {
                    string photoName = vectorTable.Columns[index];
                    result.Add(photoName);
                }
            }

            return result;
        }
    }
}