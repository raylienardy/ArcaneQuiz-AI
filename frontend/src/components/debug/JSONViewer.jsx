import { useState } from "react";

export default function JSONViewer({ data }) {
  const [collapsed, setCollapsed] = useState(true);
  const jsonString = JSON.stringify(data, null, 2);

  return (
    <div className="json-viewer">
      <button onClick={() => setCollapsed(!collapsed)} className="collapse-btn">
        {collapsed ? "▶ Show" : "▼ Hide"} JSON
      </button>
      {!collapsed && <pre className="json-content">{jsonString}</pre>}
    </div>
  );
}
