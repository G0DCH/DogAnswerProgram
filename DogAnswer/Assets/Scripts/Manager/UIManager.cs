using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace DogAnswer
{
    public class UIManager: Utility.Singleton<UIManager>
    {
        public void Close(GameObject target)
        {
            target.SetActive(false);
        }
    }
}