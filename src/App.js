import logo from './logo.svg';
import './App.css';
import { useEffect, useInsertionEffect, useRef, useState } from 'react';
import axios from 'axios';

function App() {
  const [input, setInput] = useState("");
  const [blobURL, setBlobURL] = useState("");
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isEndModel, setIsEndModel] = useState(false);
  const [loadingResult, setLoadingResult] = useState(false);

  const timer = useRef(null);

  const onSubmit = async (e) => {
    e.preventDefault();

    const data = {
      url: input,
    }

    setLoading(true);
    const res = await axios({
      url: "https://is402main.azurewebsites.net/api/save-url?code=qnPIJsAIPUFIZfaZ0jiFyD8gIqrrLvrwXc67YXufSNECAzFulHi-FQ==",
      method: 'POST',
      headers: {
        "Access-Control-Allow-Origin": "*",
        'Content-Type': 'application/json; charset=utf-8',
      },
      withCredentials: false,
      data: JSON.stringify(data),
    })
    if (res) {
      setBlobURL(res.data);
      setLoading(false);
    }
  }

  const onPredict = async (e) => {
    e.preventDefault();
    setLoadingResult(true);
    setIsEndModel(false);
    const res = await axios({
      url: `https://model.ndxcode.tk/predict?blob_url=${blobURL}`,
      method: 'GET',
      // timeout: 200000,
      headers: {
        "Access-Control-Allow-Origin": "*",
        'Content-Type': 'application/json; charset=utf-8',
      },
    })
    if (res && res?.data) {
      setIsEndModel(true);
    }
  }

  useEffect(() => {
    if (isEndModel)
      timer.current = setInterval(async () => {
        try {
          const result = await axios({
            url: `https://results.ndxcode.tk/result?url=${input}`,
            method: 'GET',
            headers: {
              "Access-Control-Allow-Origin": "*",
              'Content-Type': 'application/json; charset=utf-8',
            },
          })
          if (result?.data?.data) {
            console.log(result?.data);
            setResult(result?.data.data);
          } else {
            const result = await axios({
              url: `https://results.ndxcode.tk/result?url=${input}`,
              method: 'GET',
              headers: {
                "Access-Control-Allow-Origin": "*",
                'Content-Type': 'application/json; charset=utf-8',
              },
            })
            if (result?.data?.data) {
              console.log(result?.data);
              setResult(result?.data.data);
            }
          }
        } catch (e) {
          const result = await axios({
            url: `https://results.ndxcode.tk/result?url=${input}`,
            method: 'GET',
            headers: {
              "Access-Control-Allow-Origin": "*",
              'Content-Type': 'application/json; charset=utf-8',
            },
          })
          if (result?.data?.data) {
            console.log(result?.data);
            setResult(result?.data.data);
          }
        }
      }, 5000);

    // clear on component unmount
    return () => {
      clearInterval(timer.current);
    };

  }, [isEndModel]);

  return (
    <div className="wrapper">
      <div className="wrapper__welcome">
        <div className="wrapper__welcome--black">Enter a link youtube URL</div>

      </div>
      <form className="wrapper__form" target="_self" id="formElem">
        <div className="form__item">
          <div className="form__item--input">
            <input type="text" required name="url" value={input} onChange={(e) => { setInput(e.target.value) }} />
            <label>Link URL</label>
          </div>

        </div>

        <button className="form__button--gradients" onClick={onSubmit}>Submit</button>

      </form>
      {
        blobURL && blobURL !== "" ? (
          <form className="wrapper__form" target="_self" name="formElem1">
            <div className="form__item">
              <div className="form__item--input">
                <input type="text" required name="blob_url" value={blobURL} readOnly />
              </div>
            </div>
            <button className="form__button--gradients" onClick={onPredict}> Detect Hate Speech</button>
          </form>) : (loading ? <>Loading...</> : <></>
        )
      }

      {
        result && result.length > 0 ?
          <div style={{ height: "500px", overflowY: "auto" }}>
            <table className="wrapper__table">

              <thead>
                <tr>
                  <th>Bình Luận</th>
                  <th>Kết quả</th>
                </tr>
              </thead>
              <tbody>
                {
                  result?.map((item, index) => (
                    <tr key={index}>
                      <td style={{ color: item?.label_id === "2" ? "red" : item?.label_id === "1" ? "orange" : "black" }}>{item?.comment}</td>
                      <td style={{ color: item?.label_id === "2" ? "red" : item?.label_id === "1" ? "orange" : "black", padding: "0 10px" }}>{item?.label_id === "2" ? "hate" : item?.label_id === "1" ? "offensive" : "clean"}</td>
                    </tr>
                  ))
                }
              </tbody>
            </table>
          </div> : (loadingResult ? <>Loading...</> : <></>
          )
      }

    </div >

  );
}

export default App;
