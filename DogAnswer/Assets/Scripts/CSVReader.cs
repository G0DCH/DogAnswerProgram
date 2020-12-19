using UnityEngine;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace DogAnswer
{
    public class VectorTable
    {
        /// <summary>
        /// 앞이 헤더, 뒤가 인덱스
        /// </summary>
        public Dictionary<KeyValuePair<string, string>, float> Table;
        public List<string> Columns;
        public List<string> Rows;

        // 헤더 검색
        public Dictionary<string, List<float>> ColumnTable;
        // 인덱스 검색
        public Dictionary<string, List<float>> RowTable;
    }

    public class CSVReader
    {

        public static string SPLIT_RE = @",(?=(?:[^""]*""[^""]*"")*(?![^""]*""))";
        public static string LINE_SPLIT_RE = @"\r\n|\n\r|\n|\r";
        public static char[] TRIM_CHARS = { '\"' };

        public static VectorTable Read(string file)
        {
            VectorTable vectorTable = new VectorTable();
            var table = new Dictionary<KeyValuePair<string, string>, float>();
            TextAsset data = Resources.Load(file) as TextAsset;

            var lines = Regex.Split(data.text, LINE_SPLIT_RE);
            var rows = new List<string>();

            Dictionary<string, List<float>> columnTable = new Dictionary<string, List<float>>();
            Dictionary<string, List<float>> rowTable = new Dictionary<string, List<float>>();

            if (lines.Length <= 1)
            {
                return vectorTable;
            }

            // 헤더 분리
            var header = Regex.Split(lines[0], SPLIT_RE);

            // 헤더 리스트 추가
            List<string> columns = new List<string>(header);
            columns.RemoveAt(0);

            string rowName = string.Empty;
            for (var i = 1; i < lines.Length; i++)
            {
                List<float> rowValues = new List<float>();
                // 값 분리
                var values = Regex.Split(lines[i], SPLIT_RE);
                if (values.Length == 0 || values[0] == "") continue;

                for (var j = 0; j < header.Length && j < values.Length; j++)
                {
                    if (j == 0)
                    {
                        rowName = values[j];
                        rows.Add(values[j]);
                        continue;
                    }

                    string value = values[j];
                    value = value.TrimStart(TRIM_CHARS).TrimEnd(TRIM_CHARS).Replace("\\", "");
                    float finalvalue = float.Parse(value);

                    KeyValuePair<string, string> keySet = new KeyValuePair<string, string>(columns[j - 1], rowName);
                    // 테이블에 추가
                    table.Add(keySet, finalvalue);
                    rowValues.Add(finalvalue);

                    // 해당 헤더에 해당하는 값 추가
                    if(rowTable.TryGetValue(header[j], out List<float> columnList))
                    {
                        columnList.Add(finalvalue);
                    }
                    else
                    {
                        rowTable.Add(header[j], new List<float>());
                        columnList = rowTable[header[j]];
                        columnList.Add(finalvalue);
                    }
                }

                columnTable.Add(rowName, rowValues);
                Debug.Log(i);
            }

            vectorTable.Table = table;
            vectorTable.Rows = rows;
            vectorTable.Columns = columns;
            vectorTable.RowTable = rowTable;
            vectorTable.ColumnTable = columnTable;

            return vectorTable;
        }
    }
}