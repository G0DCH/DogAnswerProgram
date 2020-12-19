using UnityEngine;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace DogAnswer
{
    public class VectorTable
    {
        public string DogName = string.Empty;

        /// <summary>
        /// 앞이 헤더, 뒤가 인덱스
        /// </summary>
        public Dictionary<KeyValuePair<string, string>, float> Table;
        /// <summary>
        /// 헤더
        /// </summary>
        public List<string> Columns;
        /// <summary>
        /// 인덱스
        /// </summary>
        public List<string> Rows;

        /// <summary>
        /// 헤더가 인풋값
        /// </summary>
        public Dictionary<string, List<float>> ColumnTable;

        /// <summary>
        /// 인덱스가 인풋값
        /// </summary>
        public Dictionary<string, List<float>> RowTable;
    }

    public class CSVReader
    {
        public static string SPLIT_RE = @",(?=(?:[^""]*""[^""]*"")*(?![^""]*""))";
        public static string LINE_SPLIT_RE = @"\r\n|\n\r|\n|\r";
        public static char[] TRIM_CHARS = { '\"' };

        public static List<VectorTable> Read(string file)
        {
            List<VectorTable> vectorTables = new List<VectorTable>();
            var datas = Resources.LoadAll<TextAsset>(file);

            foreach (var data in datas)
            {
                VectorTable vectorTable = new VectorTable();
                var table = new Dictionary<KeyValuePair<string, string>, float>();

                var lines = Regex.Split(data.text, LINE_SPLIT_RE);
                var rows = new List<string>();

                Dictionary<string, List<float>> columnTable = new Dictionary<string, List<float>>();
                Dictionary<string, List<float>> rowTable = new Dictionary<string, List<float>>();

                if (lines.Length <= 1)
                {
                    continue;
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
                        if (rowTable.TryGetValue(header[j], out List<float> columnList))
                        {
                            columnList.Add(finalvalue);
                        }
                        else
                        {
                            rowTable.Add(header[j], new List<float>());
                            rowTable[header[j]].Add(finalvalue);
                        }
                    }

                    columnTable.Add(rowName, rowValues);
                }

                vectorTable.DogName = data.name;
                vectorTable.Table = table;
                vectorTable.Rows = rows;
                vectorTable.Columns = columns;
                vectorTable.RowTable = rowTable;
                vectorTable.ColumnTable = columnTable;

                vectorTables.Add(vectorTable);
            }
            return vectorTables;
        }
    }
}