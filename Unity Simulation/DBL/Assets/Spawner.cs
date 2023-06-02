using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner : MonoBehaviour
{

    public GameObject blackCube;
    public GameObject whiteCube;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            int random = Random.Range(0, 2);
            Debug.Log(random);
            if (random == 1)
            {
                Instantiate(blackCube, gameObject.transform.position, Quaternion.identity);
            } else
            {
                Instantiate(whiteCube, gameObject.transform.position, Quaternion.identity);
            }
        }
    }
}
