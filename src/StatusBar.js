function StatusBarItem({text}) {
    return (
        <div className="StatusBarItem">
        {text}
        </div>
    )   
}

function StatusBar() {
  return (
    <div className="StatusBar">
        <StatusBarItem text="Nie ma sera @Piotr kup ser"/>
    </div>
  )
}

export default StatusBar;