import React from 'react';
import { useState } from 'react';
import './group-forms.css'
import axios from 'axios';

function Usergroupsform({mode}) {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [formData, setFormData] = useState({
        user_label: '',
        expectation_id: '',
        expectation_verb: '',
        object_type: '',
        context_attributes: [{ contextAttribute: 'TargetSDV', contextCondition: 'IS_EQUAL_TO', contextValueRange: [] }],
        target_metrics: [{ targetName: 'Speed', targetCondition: 'IS_REPORTED', targetValueRange: '' }],
        priority: '',
        location: '',
        observation_period: '',
        report_reference: ''
      });

    // variables and functions to handle the submit button and connect to MONGODB
    const openModal = () => {
        setModalIsOpen(true);
    };
    
      const closeModal = () => {
        setModalIsOpen(false);
    };
    const preSubmit = (e) => {
        e.preventDefault()
        openModal();
    };
    const isFormValid = () => {
      return (
        formData.user_label &&
        formData.expectation_id &&
        formData.expectation_verb &&
        formData.object_type &&
        formData.context_attributes[0].contextValueRange.length > 0 &&
        formData.priority &&
        formData.location &&
        formData.observation_period &&
        formData.report_reference
      );
    };
    const handleSubmit = async (e) => {
      e.preventDefault()
        
        console.log(formData)
        try {
          // Send formData (JSON) to Django backend
          const response = await fetch('http://127.0.0.1:8000/api/ApplicationIntent/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
          });
    
          if (response.ok) {
            const result = await response.json();
            alert('File uploaded successfully!');
            console.log(result);
          } else {
            alert('Failed to upload file.');
          }
        } catch (error) {
          console.error('Error:', error);
          alert('An error occurred while uploading the file.');
        }
    
    }

  return (
    <div style={{margin:"20px"}}>
        {/* form to submit the user-group part */}
      <form onSubmit={handleSubmit}>
        <div>
          <label>User Label (String, required)</label>
          <select name="user_label" value={formData.user_label} onChange={(e) => setFormData({ ...formData, user_label: e.target.value })}>
            <option value="">Select User Label</option>
            <option value="Retrieve SDV Speed">Retrieve SDV Speed</option>
            <option value="Monitor SDV Position">Monitor SDV Position</option>
          </select>
        </div><br></br>
        <div>
          <label>Expectation ID (String, required)</label>
          <select name="expectation_id" value={formData.expectation_id} onChange={(e) => setFormData({ ...formData, expectation_id: e.target.value })}>
            <option value="">Select Expectation ID</option>
            <option value="1">1</option>
            <option value="2">2</option>
          </select>
        </div><br></br>
        <div>
          <label>Expectation Verb (Enum: DELIVER, ENSURE, required)</label>
          <select name="expectation_verb" value={formData.expectation_verb} onChange={(e) => setFormData({ ...formData, expectation_verb: e.target.value })}>
            <option value="">Select Expectation Verb</option>
            <option value="DELIVER">DELIVER</option>
            <option value="ENSURE">ENSURE</option>
          </select>
        </div><br></br>
        <div>
          <label>Object Type (Enum, required)</label>
          <select name="object_type" value={formData.object_type} onChange={(e) => setFormData({ ...formData, object_type: e.target.value })}>
            <option value="">Select Object Type</option>
            <option value="SDV">SDV</option>
            <option value="RAN">RAN</option>
          </select>
        </div><br></br>
        <div>
        <label>Target SDV ID (String, required)</label>
          <div>
            <label>
              <input
                type="checkbox"
                value="SDV_001"
                checked={formData.context_attributes[0].contextValueRange.includes("SDV_001")}
                onChange={(e) => {const updatedContextAttributes = [...formData.context_attributes]; 
                  if (e.target.checked) {
                    updatedContextAttributes[0].contextValueRange.push(e.target.value);} 
                    else {
                      updatedContextAttributes[0].contextValueRange = updatedContextAttributes[0].contextValueRange.filter(val => val !== e.target.value);}
                      updatedContextAttributes[0].contextValueRange.sort();
                      setFormData({ ...formData, context_attributes: updatedContextAttributes });
              }}
              />
              SDV_001
            </label><br></br>
            <label>
              <input
                type="checkbox"
                value="SDV_002"
                checked={formData.context_attributes[0].contextValueRange.includes("SDV_002")}
                onChange={(e) => {
                  const updatedContextAttributes = [...formData.context_attributes];
                  if (e.target.checked) {
                    updatedContextAttributes[0].contextValueRange.push(e.target.value);} 
                    else {
                      updatedContextAttributes[0].contextValueRange = updatedContextAttributes[0].contextValueRange.filter(val => val !== e.target.value);
                    }
                    updatedContextAttributes[0].contextValueRange.sort();
                    setFormData({ ...formData, context_attributes: updatedContextAttributes });
                  }}
              />
              SDV_002
            </label><br></br>
            <label>
              <input
                type="checkbox"
                value="SDV_003"
                checked={formData.context_attributes[0].contextValueRange.includes("SDV_003")}
                onChange={(e) => {
                  const updatedContextAttributes = [...formData.context_attributes];
                  if (e.target.checked) {
                    updatedContextAttributes[0].contextValueRange.push(e.target.value);} 
                    else {
                      updatedContextAttributes[0].contextValueRange = updatedContextAttributes[0].contextValueRange.filter(val => val !== e.target.value);
                    }
                    updatedContextAttributes[0].contextValueRange.sort();
                    setFormData({ ...formData, context_attributes: updatedContextAttributes });
                  }}
              />
              SDV_003
            </label>
          </div>
        </div><br></br>
        <div>
          <label>Speed Value (String, optional)</label>
          <select name="target_metrics[0].targetValueRange" value={formData.target_metrics[0].targetValueRange} onChange={(e) => {
            const updatedTargetMetrics = [...formData.target_metrics];
            updatedTargetMetrics[0].targetValueRange = e.target.value;
            setFormData({ ...formData, target_metrics: updatedTargetMetrics });
          }}>
            <option value="">Select Speed Value</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </div><br></br>
        <div>
          <label>Priority (Integer, 1-100, required)</label>
          <select name="priority" value={formData.priority} onChange={(e) => setFormData({ ...formData, priority: e.target.value })}>
            <option value="">Select Priority</option>
            {[...Array(100).keys()].map((i) => (
              <option key={i + 1} value={i + 1}>{i + 1}</option>
            ))}
          </select>
        </div><br></br>
        <div>
          <label>Location (GPS Coordinates system, required)</label>
          <select name="observation_period" value={formData.location} onChange={(e) => setFormData({ ...formData, location: e.target.value })}>
            <option value="">Select Observation Period</option>
            <option value="Geographic Coordinate System">Geographic Coordinate System</option>
            <option value="Cartesian Coordinate System">Cartesian Coordinate System</option>
          </select>
        </div><br></br>
        <div>
          <label>Observation Period (Integer, in seconds, required)</label>
          <select name="observation_period" value={formData.observation_period} onChange={(e) => setFormData({ ...formData, observation_period: e.target.value })}>
            <option value="">Select Observation Period</option>
            <option value="30">30</option>
            <option value="60">60</option>
            <option value="120">120</option>
          </select>
        </div><br></br>
        <div>
          <label>Report Reference (String, required)</label>
          <select name="report_reference" value={formData.report_reference} onChange={(e) => setFormData({ ...formData, report_reference: e.target.value })}>
            <option value="">Select Report Reference</option>
            <option value="IntentReport_001">IntentReport_001</option>
            <option value="IntentReport_002">IntentReport_002</option>
          </select>
        </div><br></br>



        <footer className='footer'>
          <button
            className={isFormValid() ? (mode === 'dark' ? 'dark-button' : 'light-button') : 'disabled-button'}
            type='submit'
            disabled={!isFormValid()}
            style={{
              backgroundColor: isFormValid() ? '' : 'gray',
              color: isFormValid() ? '' : 'white',
              border: isFormValid() ? '' : 'solid 1px #ccc'
            }}
          >
            Submit
          </button>
        </footer>
        </form>
    </div>
  )
}

export default Usergroupsform;
        // try {
        //     const response = await axios.post('http://localhost:5000/create_intent', formData);
        //     console.log('Intent created:', response.data);
        //     closeModal();
        //   } catch (error) {
        //     console.error('Error creating intent:', error);
        //   }
          
        // var mac = document.getElementById("macBox")
        // var startipv4 = document.getElementById("startIPv4")
        // var endipv4 = document.getElementById("endIPv4")
        // var startipv6 = document.getElementById("startIPv6")
        // var endipv6 = document.getElementById("endIPv6")

        // let checkForm = true;
        // if (form["mac-address"]!=null) {
        //     if (!validateMAC(form["mac-address"])) {
        //         mac.style.color = "red";
        //         checkForm = false;
        //     }
        //     else {
        //         if (mode === "dark") {
        //             mac.style.color = "black";
        //         }
                
        //     }
        // }

        // if (form["range-ipv4-address"]["start"]!=null){
        //     if (!validateIPv4(form["range-ipv4-address"]["start"])){
        //         startipv4.style.color = "red";
        //         checkForm = false;
        //     }
        //     else {
        //         startipv4.style.color = "black";
        //     }
        // }
        // if (form["range-ipv4-address"]["end"]!=null) {
        //     if (!validateIPv4(form["range-ipv4-address"]["end"])){
        //         endipv4.style.color = "red";
        //         checkForm = false;
        //     }
        //     else {
        //         endipv4.style.color = "black";
        //     }
        // }

        // if (form["range-ipv6-address"]["start"]!=null) {
        //     if (!validateIPv6(form["range-ipv6-address"]["start"])) {
        //         startipv6.style.color = "red";
        //         checkForm = false;
        //     }
        //     else {
        //         startipv6.style.color = "black";
        //     }
        // }
        // if (form["range-ipv6-address"]["end"]!=null) {
        //     if (!validateIPv6(form["range-ipv6-address"]["end"])) {
        //         endipv6.style.color = "red";
        //         checkForm = false;
        //     }
        //     else {
        //         endipv6.style.color = "black";
        //     }
        // }

        // if (form["range-ipv6-address"]["start"] === null && form["range-ipv4-address"]["start"] === null && form["mac-address"] === null) {
        //     checkForm = false;
        //     alert("At least one of MAC/IPv4/IPv6 address must be filled")
        // }

        // 'http://115.145.178.185:5000/user/put'