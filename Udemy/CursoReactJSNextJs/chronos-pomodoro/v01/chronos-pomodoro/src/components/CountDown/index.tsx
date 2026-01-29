import { useTaskContext } from '../../contexts/TaskContext/useTaskContext';
import styles from './styles.module.css';

export function CountDown() {
  const { state, setState } = useTaskContext();
  /*
  function handleClick() {
    setState(prev => {
      return {
        ...prev,
        formattedSecondsRemaining: 'Abacaxi',
      };
    });
  }
  return (
    <>
      <button onClick={handleClick}>TESTE</button>
      <div className={styles.container}>{state.formattedSecondsRemaining}</div>
    </>
  );
  */
  return (
    <div className={styles.container}>{state.formattedSecondsRemaining}</div>
  );
}
