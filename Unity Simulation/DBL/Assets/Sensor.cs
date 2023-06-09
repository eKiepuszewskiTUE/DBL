using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Sensor : MonoBehaviour
{

    // Update is called once per frame

    private float delay;

    private void Start()
    {
        delay = 2f;
    }

    private void FixedUpdate()
    {
        Vector3 fwd = transform.TransformDirection(Vector3.forward) * 10;
        RaycastHit hit;

        if (Physics.Raycast(transform.position, fwd, out hit))
        {
            print("There is something in front of the object!");
            Debug.Log(hit.collider.gameObject.tag);
            if (hit.collider.gameObject.tag == "BlackCube")
            {
                StartCoroutine(turnL(delay));
                
            } else if (hit.collider.gameObject.tag == "WhiteCube")
            {
                StartCoroutine(turnR(delay));               
            }

        }
    }

    void Update()
    {
        Vector3 forward = transform.TransformDirection(Vector3.forward) * 10;
        Debug.DrawRay(transform.position, forward, Color.green);
    }


    IEnumerator turnL(float seconds)
    {
        yield return new WaitForSeconds(seconds);
        Splitter.instance.rotation = false;
    }

    IEnumerator turnR(float seconds)
    {
        yield return new WaitForSeconds(seconds);
        Splitter.instance.rotation = true;
    }
}
