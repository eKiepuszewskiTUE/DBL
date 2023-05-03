using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ConveyorBelt : MonoBehaviour
{
    public float speed;
    public float visualSpeedScalar;

    private Vector3 direction;
    private float currentScroll;
    private Rigidbody rb;

    List<GameObject> onBelt;

    private void Start()
    {
        currentScroll = 0f;
        rb = GetComponent<Rigidbody>();
        onBelt = new List<GameObject>();
    }

    private void Update()
    {
        // Scroll texture to fake it moving
        currentScroll = currentScroll + Time.deltaTime * speed * visualSpeedScalar;
        GetComponent<Renderer>().material.mainTextureOffset = new Vector2(0, currentScroll);
    }

    private void FixedUpdate()
    {
        direction = transform.forward;
        for (int i = 0; i < onBelt.Count; i++)
        {
            onBelt[i].gameObject.GetComponent<Rigidbody>().AddForce(speed * direction);
        }
    }

    // Anything that is touching will move
    // This function repeats as long as the object is touching


    private void OnCollisionEnter(Collision collision)
    {
        onBelt.Add(collision.gameObject);
    }

    private void OnCollisionExit(Collision collision)
    {
        onBelt.Remove(collision.gameObject);
    }

    /*
    private void OnCollisionStay(Collision otherThing)
    {
        Debug.Log(otherThing);

        

        // Get the direction of the conveyor belt 
        // (transform.forward is a built in Vector3 
        // which is used to get the forward facing direction)
        // * Remember Vector3's can used for position AND direction AND rotation
        

        otherThing.gameObject.GetComponent<Rigidbody>().AddForce(speed * direction);

        // Add a WORLD force to the other objects
        // Ignore the mass of the other objects so they all go the same speed (ForceMode.Acceleration)
        //otherThing.gameObject.GetComponent<Rigidbody>().AddForce(direction * speed, ForceMode.Acceleration);

        //otherThing.gameObject.GetComponent<Rigidbody>().velocity = speed * direction * Time.deltaTime * 50f;
    }
    */
}
