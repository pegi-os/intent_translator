import React from 'react';
import NaturalIntentForm from './natural-intent-form';
import "./modal.css";
import styled from "styled-components";

const Title = styled.h1`
  font-size: 1.5em;
  text-align: center;
`;

function NaturalModal({ closeNaturalModal, mode }) {
  return (
    <div className="modalBackground">
      <div className={mode === 'dark' ? 'dark-modalContainer' : 'light-modalContainer'}>
        
        {/* 닫기 버튼 */}
        <button className="closeModalBtn" onClick={() => closeNaturalModal(false)}>
          X
        </button>

        <Title>Natural Language Intent</Title>

        <div className="body">
          <NaturalIntentForm mode={mode} closeNaturalModal={closeNaturalModal}/>
        </div>
      </div>
    </div>
  );
}

export default NaturalModal;
