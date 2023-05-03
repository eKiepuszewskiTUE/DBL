using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Windmill : MonoBehaviour
{
    public float rotationSpeed;
    Rigidbody rb;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Vector3 rotation = new Vector3(0f, 1f, 0f) * rotationSpeed * Time.deltaTime;
        rb.AddRelativeTorque(rotation, ForceMode.Impulse);
    }
}
