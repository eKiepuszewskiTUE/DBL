using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Sensor : MonoBehaviour
{

    // Update is called once per frame

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
                Splitter.instance.rotation = false;
            } else if (hit.collider.gameObject.tag == "WhiteCube")
            {
                Splitter.instance.rotation = true;
            }

        }
    }

    void Update()
    {
        Vector3 forward = transform.TransformDirection(Vector3.forward) * 10;
        Debug.DrawRay(transform.position, forward, Color.green);
    }
}
