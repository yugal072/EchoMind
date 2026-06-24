import os
from pathlib import Path
from langchain_core.documents import Document
from datetime import datetime
from typing import List, Dict

def get_sms_to_documents(sms_messages:List[Dict])->List[Document]:
    documents = []
    
    for sms in sms_messages:
        try:
            #extract key fields from termux sms format
            body = sms.get("body","")
            sender = sms.get("sender", "unknown")
            timestamp = sms.get("timestamp",None) or sms.get("received")
            received_at = sms.get("received", None)
            
            if not body.strip():
                continue      # skip empty messages
            
            if timestamp:
                try:
                    dt = datetime.fromtimestamp(int[timestamp]/1000)
                    date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                
            metadata = {
                "source": "sms",
                "sender": sender,
                "timestamp": date_str,
                "message_id":sms.get("id") or f"sms_{datetime.now().timestamp()}",
                "type":"inbound" if sms.get("type") == 1 else "outbound",
                "ingested_at": datetime.now().isoformat()
            }
            
            doc = Document(
                page_content=body.strip(),
                metadata = metadata
            )
            documents.append(doc)
        except Exception as e:
            print(f"Failed to parse one sms: {e}")         
            continue
           
    print(f"✅ Parsed {len(documents)} SMS messages into documents")
    return documents