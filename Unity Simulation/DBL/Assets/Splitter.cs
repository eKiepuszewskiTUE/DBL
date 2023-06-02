using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Splitter : MonoBehaviour
{

    public bool rotation;

    public static Splitter instance;
    public void Awake()
    {
        if (instance != null)
        {
            Destroy(instance);
        } else
        {
            instance = this;
        }
        DontDestroyOnLoad(gameObject);
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (rotation)
        {
            Quaternion target = Quaternion.Euler(25, 38, 150);
            gameObject.transform.rotation = Quaternion.Slerp(transform.rotation, target, Time.deltaTime * 10f);
        } else
        {
            Quaternion target = Quaternion.Euler(-25, -38, 150);
            gameObject.transform.rotation = Quaternion.Slerp(transform.rotation, target, Time.deltaTime * 10f);
        }
    }
}
