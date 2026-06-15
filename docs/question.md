Well now I am gonna give you my dataset.json and results.json where dataset.json is one hand written by me and the results.json is one formed by RAG:
JSON[  
    {
        "question": "What emails did I receive yesterday from placement@viit.ac.in?",
        "answer": ["You received an email from placement@viit.ac.in regarding the placement opportunity at PACCAR india + performance based PPO. The deadline for the placement application is 12th June 2026.The email was sent on 2026-06-01 at 10:00 AM. The email also includes 3 documents for JD and details of the company and job role.", "You received another email from placement@viit.ac.in regarding the placement opportunities for final year female students. The Meesho's hackathon will be conducted before June 19. By applying at this link[](https://scoutit.in/apply/meesho-hiring-challenge-2026), the students can win jobs, internships, and a trip to Bengaluru."]
    },
    {
        "question": "What is the deadline for the placement application at PACCAR?",
        "answer": "The deadline for the placement application at PACCAR is 12th June 2026."
    },
    {
        "question": "Did I receive any emails from Placement VIIT yesterday?",
        "answer": "Yes, you received two emails from the placement cell at VIIT yesterday. One email was regarding the placement opportunity at PACCAR india + performance based PPO, and the other email was about placement opportunities in Meesho for final year female students, including Meesho's hackathon."
    },
    {
        "question": "What emails did I receive from internship@viit.ac.in today and what are they?",
        "answer": "Yes, you received an email from internship cell. There is an opportunity to join a free 30-day Electric Vehicle (EV) training program happening at the VIT campus for final-year students in the CSE-IoT, CSBT, Mechanical, Instrumentation, or E&TC branches. Successfully completing this training makes you eligible for a 3-month paid internship with a stipend of up to ₹22,000 per month. You can register today by filling out this Google form: https://docs.google.com/forms/d/e/1FAIpQLSfxPb5zryCwlFLO3NFQT7HjjZ6qC3ehIPAAwGyDEYy6D7va5Q/viewform?usp=publish-editor. "
    },
    {
        "question": "What is the deadline for the Meesho's hackathon?",
        "answer": "The deadline for the Meesho's hackathon is before June 19, 2026."
    },
    {
        "question": "What other important emails did i recieve in last few days?",
        "answer": "You received three important emails recently. First, on May 6, the Students' Section sent the college opening letter for Final Year B.Tech (Semester I of Academic Year 2026-27). Second, on May 27, the exam cell shared the seating arrangement for the TYBTech Re-Exam and Special End Semester Exams, which are scheduled from June 1 to June 4, 2026. Finally, also on May 27, Placement VIIT sent an email regarding the registration for the ARAI Internship for the 2027 batch, with an application deadline of May 29, 2026, at 10:00 AM."
    },
    {
        "question": "who made the gpio app and whats their prn?",
        "answer": "The student's name is Yugal Upadhayay, and their PRN is 22310753[cite: 1]."
    },
    {
        "question": "gpio pins for the leds?",
        "answer": "The script uses GPIO pin 13 for the Red LED, pin 19 for the Yellow LED, and pin 26 for the Green LED[cite: 1]."
    },
    {
        "question": "bg and text color in css?",
        "answer": "The CSS sets the background color to #005f20 and the text color to #fff5ee[cite: 2]."
    },
    {
        "question": "what action turns the gpio high?",
        "answer": "Passing the \"on\" action in the URL causes the GPIO to output HIGH to the actuator[cite: 11]."
    },
    {
        "question": "what host and port is it running on?",
        "answer": "The application is configured to run on host 0.0.0.0 and port 5000[cite: 12]."
    },
    {
        "question": "where does the fast and slow title come from?",
        "answer": "The title comes from the distinction between fast and slow thinking, which corresponds to the division between the subconscious and conscious minds[cite: 24]."
    },
    {
        "question": "physical signs of slow thinking?",
        "answer": "Slow thinking takes a lot of effort and causes physical symptoms like dilated pupils, increased heart rates, and higher blood pressures[cite: 35]."
    },
    {
        "question": "what's wysiati mean?",
        "answer": "WYSIATI stands for \"what you see is all there is\"[cite: 61]."
    },
    {
        "question": "why use algorithms instead of intuition?",
        "answer": "Algorithms force you to collect more relevant information instead of just relying on what's readily available[cite: 72]. They also stop you from relying on subjective weights and prevent you from being seduced by an attractive narrative[cite: 73]."
    },
    {
        "question": "what is risk aversion here?",
        "answer": "Risk aversion is the idea that a loss is much harder to sustain than a gain, making people more likely to accept a small, secure benefit rather than risk going for a more uncertain one[cite: 173, 174]."
    }



]
 
JSON[
    {
        "question": "What emails did I receive yesterday from placement@viit.ac.in?",
        "ground_truth": [
            "You received an email from placement@viit.ac.in regarding the placement opportunity at PACCAR india + performance based PPO. The deadline for the placement application is 12th June 2026.The email was sent on 2026-06-01 at 10:00 AM. The email also includes 3 documents for JD and details of the company and job role.",
            "You received another email from placement@viit.ac.in regarding the placement opportunities for final year female students. The Meesho's hackathon will be conducted before June 19. By applying at this link[](https://scoutit.in/apply/meesho-hiring-challenge-2026), the students can win jobs, internships, and a trip to Bengaluru."
        ],
        "answer": "You received an email from placement@viit.ac.in on June 11, 2026, at 15:36:37 +0530. The subject of the email was \"Fwd: Registration  of  PACCAR India  Internship + Performance Based PPO  for   2027   batch\". \n\nThe email was from Anand Bhavsar and Priyanka More, and it was also copied to KIRAN PAWAR and Aparna Mitragotri. \n\nIf you are looking for more information or specific details about other emails, I suggest checking your email inbox or contacting the sender directly. \n\n(Source: Provided context)",
        "contexts": [
            "Subject: Fwd: Registration\u00a0\u00a0of\u00a0 PACCAR India\u00a0 Internship + Performance Based PPO\u00a0\u00a0for\u00a0 \u00a02027\u00a0 \u00a0batch .\nFrom:Placement VIIT <placement@viit.ac.in>\nDate:Thu, 11 Jun 2026 15:36:37 +0530\nText:Dear Students,\r\n\nPlease do  registration  of  PACCAR India  Internship + Performance Based\r\nPPO  for   2027   batch .\r\n\nREAD  ALL THREE   ATTACHMENTS CAREFULLY.\r\n\n*Deadline :   Tomorrow,  12th June  2026 ,   10.00 am.*",
            ", \n, \n,\r\n\n, \n, \n,\r\nAnand Bhavsar \n, Priyanka More <\r\npriyanka.more@viit.ac.in>, Placement VIIT \n,\r\nPlacements VU \n, KIRAN PAWAR <\r\nkiran.pawar@vupune.ac.in>, Aparna Mitragotri \n\nDear  FEMALE Students,\r\n\nPlease go through trailing mail and apply on the given link, if you found\r\nit suitable for you.\r\n\nAll the Best!\r\nThanks.\r\nA.S. Mitragotri\r\nTPO,\r\nVIT\r\n\n---------- Forwarded message ---------",
            "---------- Forwarded message ---------\r\nFrom: Dr. (Mrs.) Priya M. Shelke \n\nDate: Thu, 4 Jun, 2026, 2:05\u202fpm\r\nSubject: Fwd: Invitation: Free EV Training & Paid Internship Program for\r\nStudents\r\nTo: internship@viit.ac.in \n, <\r\narchana.ratnaparkhi@viit.ac.in>\r\n\nDear Archana Madam,\r\nKindly float this internship opportunity to final-year students of\r\nCSE-IoTCSBT, Mechanical, Instrumentation and Electronics &\r\nTelecommunication Engg students.\r\nIf you need any other details let me know.\r\nThank you",
            "Subject: Orientation Session - Today 8 PM for One Week Immersion Program in China\nFrom:\"'Chief International Relation Officer, VI-VU' via TY-2025-26\" <ty@viit.ac.in>\nDate:Fri, 5 Jun 2026 13:59:06 +0530\nText:Dear Students,\r\n\nWe have arranged an orientation program for understanding more details\r\nabout the Global Industry Immersion Program \u2013 China Edition\r\n\nDate - 5th June 2026 (Today)\r\n\nTime - Session starts at 8 PM\r\n\nJoining\r\n\n Link\r\n\n*"
        ]
    },
    {
        "question": "What is the deadline for the placement application at PACCAR?",
        "ground_truth": "The deadline for the placement application at PACCAR is 12th June 2026.",
        "answer": "The deadline for the PACCAR India Internship + Performance Based PPO registration is June 12, 2026, at 10:00 am. \n\nHowever, there are other deadlines mentioned for different scenarios:\n- With Flight & Visa Package: June 15, 2026\n- Without Flight Option (book on your own): June 30, 2026\n- Application Deadline for another programme: June 19, 2026 \n\nBut specifically for the PACCAR India Internship, the deadline is June 12, 2026, at 10:00 am. \n\n(Source: Provided context)",
        "contexts": [
            "Subject: Fwd: Registration\u00a0\u00a0of\u00a0 PACCAR India\u00a0 Internship + Performance Based PPO\u00a0\u00a0for\u00a0 \u00a02027\u00a0 \u00a0batch .\nFrom:Placement VIIT <placement@viit.ac.in>\nDate:Thu, 11 Jun 2026 15:36:37 +0530\nText:Dear Students,\r\n\nPlease do  registration  of  PACCAR India  Internship + Performance Based\r\nPPO  for   2027   batch .\r\n\nREAD  ALL THREE   ATTACHMENTS CAREFULLY.\r\n\n*Deadline :   Tomorrow,  12th June  2026 ,   10.00 am.*",
            "Thanks and Regards,\r\n\n*Central Training and Placement Office*\r\nVishwakarma Institutes, Pune\r\n\nWebsite: www.vit.edu\r\n\n---------- Forwarded message ---------\r\nFrom: Sadiya Akhtar\r\n\nHi Team ,\r\n\nPlease find attached the students shortlisted for the in-person internship\r\nhiring on 16th June 2026.\r\n\nPlease confirm the availability of the shortlisted students for the process.\r\n\nRegards\r\nSadiya",
            ">\r\n> As this is an international programme involving flight reservations and\r\n> visa processing, we request institutions to kindly adhere to the\r\n> registration timelines strictly.\r\n>\r\n>\r\n>\r\n> Registration Deadlines:\r\n>\r\n> With Flight & Visa Package: 15th June 2026\r\n>\r\n> Without Flight Option available (book on your own): 30th June 2026\r\n>\r\n>\r\n>\r\n> Please note that seats are limited and the programme is open to only 50\r\n> students across India.\r\n>\r\n>\r\n>\r\n> Contact Details\r\n>",
            "*Application Deadline: 19th June 2026 *\r\n\n*What\u2019s in it for the candidates?*\r\n\n1. * Internships + Full-Time Offers (PPOs)* up for grabs at Meesho\r\n2. A fully sponsored trip to Meesho HQ, Bengaluru\r\n3. Exciting Merchandise & Goodies\r\n\nWe request that you circulate this opportunity to your students before the\r\ndeadline.\r\n\n*Note: Scoutit is the event partner for Meesho ScriptedBy{Her} 2.0,\r\nassisting them in reaching relevant candidates for their hiring challenge.*\r\n\nRegards,\r\nTeam Scoutit"
        ]
    },
    {
        "question": "Did I receive any emails from Placement VIIT yesterday?",
        "ground_truth": "Yes, you received two emails from the placement cell at VIIT yesterday. One email was regarding the placement opportunity at PACCAR india + performance based PPO, and the other email was about placement opportunities in Meesho for final year female students, including Meesho's hackathon.",
        "answer": "I don't have enough information to confirm if you received any emails from Placement VIIT yesterday. The context provided does not contain information about your email activity or any emails sent to you from Placement VIIT yesterday. \n\nHowever, I can see that there are some emails related to placements and internships from various senders, including Central Training and Placement Office, Vishwakarma Institutes, Pune, and others. \n\nIf you are looking for specific information about emails you received, I suggest checking your email inbox.",
        "contexts": [
            "Thanks and Regards,\r\n\n*Central Training and Placement Office*\r\nVishwakarma Institutes, Pune\r\n\nWebsite: www.vit.edu\r\n\n---------- Forwarded message ---------\r\nFrom: Sadiya Akhtar\r\n\nHi Team ,\r\n\nPlease find attached the students shortlisted for the in-person internship\r\nhiring on 16th June 2026.\r\n\nPlease confirm the availability of the shortlisted students for the process.\r\n\nRegards\r\nSadiya",
            "Subject: Orientation Session - Today 8 PM for One Week Immersion Program in China\nFrom:\"'Chief International Relation Officer, VI-VU' via TY-2025-26\" <ty@viit.ac.in>\nDate:Fri, 5 Jun 2026 13:59:06 +0530\nText:Dear Students,\r\n\nWe have arranged an orientation program for understanding more details\r\nabout the Global Industry Immersion Program \u2013 China Edition\r\n\nDate - 5th June 2026 (Today)\r\n\nTime - Session starts at 8 PM\r\n\nJoining\r\n\n Link\r\n\n*",
            "---------- Forwarded message ---------\r\nFrom: Dr. (Mrs.) Priya M. Shelke \n\nDate: Thu, 4 Jun, 2026, 2:05\u202fpm\r\nSubject: Fwd: Invitation: Free EV Training & Paid Internship Program for\r\nStudents\r\nTo: internship@viit.ac.in \n, <\r\narchana.ratnaparkhi@viit.ac.in>\r\n\nDear Archana Madam,\r\nKindly float this internship opportunity to final-year students of\r\nCSE-IoTCSBT, Mechanical, Instrumentation and Electronics &\r\nTelecommunication Engg students.\r\nIf you need any other details let me know.\r\nThank you",
            "Subject: Re: Orientation Session - Today 8 PM for One Week Immersion Program in China\nFrom:\"'Chief International Relation Officer, VI-VU' via TY-2025-26\" <ty@viit.ac.in>\nDate:Fri, 5 Jun 2026 19:50:04 +0530\nText:Dear Students,\r\nGentle reminder to join the session at 8 PM.\r\n\nOn Fri, 5 Jun 2026, 13:59 Chief International Relation Officer, VI-VU, <\r\nciro@vit.edu> wrote:"
        ]
    },
    {
        "question": "What emails did I receive from internship@viit.ac.in today and what are they?",
        "ground_truth": "Yes, you received an email from internship cell. There is an opportunity to join a free 30-day Electric Vehicle (EV) training program happening at the VIT campus for final-year students in the CSE-IoT, CSBT, Mechanical, Instrumentation, or E&TC branches. Successfully completing this training makes you eligible for a 3-month paid internship with a stipend of up to \u00e2\u201a\u00b922,000 per month. You can register today by filling out this Google form: https://docs.google.com/forms/d/e/1FAIpQLSfxPb5zryCwlFLO3NFQT7HjjZ6qC3ehIPAAwGyDEYy6D7va5Q/viewform?usp=publish-editor. ",
        "answer": "I don't have information about the emails you received today. However, I can see that there are a few emails from internship@viit.ac.in and other related senders in the provided context:\n\n1. An email inviting students to a Free EV Training & Paid Internship Program, sent by Dr. Archana Ratnaparkhi, VIIT Internship Coordinator.\n2. A forwarded message regarding the same internship opportunity, sent by Dr. (Mrs.) Priya M. Shelke.\n\nThese emails seem to be related to internship opportunities, but I don't have information about the emails you received specifically today. \n\nIf you are looking for specific information about your emails, I suggest checking your email inbox.",
        "contexts": [
            "Thanks and Regards,\r\n\n*Central Training and Placement Office*\r\nVishwakarma Institutes, Pune\r\n\nWebsite: www.vit.edu\r\n\n---------- Forwarded message ---------\r\nFrom: Sadiya Akhtar\r\n\nHi Team ,\r\n\nPlease find attached the students shortlisted for the in-person internship\r\nhiring on 16th June 2026.\r\n\nPlease confirm the availability of the shortlisted students for the process.\r\n\nRegards\r\nSadiya",
            "Subject: Fwd: Invitation: Free EV Training & Paid Internship Program for Students\nFrom:Internship VIIT <internship@viit.ac.in>\nDate:Sun, 7 Jun 2026 18:22:19 +0530\nText:Pls check the opportunity and fill the Google form today itself.\r\n\nDr.Archana Ratnaparkhi\r\n\nVIIT Internship Coordinator\r\nVIIT,Pune\r\narchana.ratnaparakhi@viit.ac.in\r\n8605432488\r\n\n---------- Forwarded message ---------\r\nFrom: Dr. (Mrs.) Priya M. Shelke",
            "Subject: Colgate Palmolive -Internship Campus Recruitment 2026-27\nFrom:\"TPO - Vishwakarma Institute of Technology, Pune\" <tpo_students@vit.edu>\nDate:Wed, 10 Jun 2026 14:57:44 +0530\nText:Dear students,\r\n*Please find attached the students shortlisted for the in-person internship\r\nhiring on 16th June 2026.*\r\nRead the mail carefully\r\nFurther details will be shared with you shortly.\r\n*Confirm your acceptance today till 4:00pm .*\r\n\n Thanks and Regards,",
            "---------- Forwarded message ---------\r\nFrom: Dr. (Mrs.) Priya M. Shelke \n\nDate: Thu, 4 Jun, 2026, 2:05\u202fpm\r\nSubject: Fwd: Invitation: Free EV Training & Paid Internship Program for\r\nStudents\r\nTo: internship@viit.ac.in \n, <\r\narchana.ratnaparkhi@viit.ac.in>\r\n\nDear Archana Madam,\r\nKindly float this internship opportunity to final-year students of\r\nCSE-IoTCSBT, Mechanical, Instrumentation and Electronics &\r\nTelecommunication Engg students.\r\nIf you need any other details let me know.\r\nThank you"
        ]
    },
    {
        "question": "What is the deadline for the Meesho's hackathon?",
        "ground_truth": "The deadline for the Meesho's hackathon is before June 19, 2026.",
        "answer": "The deadline for Meesho's ScriptedBy{Her} 2.0 Hackathon application is June 19, 2026.\n\n(Source: Provided context)",
        "contexts": [
            "*Meesho* is inviting applications for their * ScriptedBy{Her} 2.0 Hackathon*\r\n\n,\r\nwhere students will stand a chance to get *Internships & Full-Time Offers\r\n(PPOs)*.\r\n\n*Application Link: \r\n\n*\r\n\n*Eligibility: Final-year female students (2027 batch) from B.E./B.Tech.\r\nprograms *\r\n\n*Application Deadline: 19th June 2026 *\r\n\n*What\u2019s in it for the candidates?*",
            "*Application Deadline: 19th June 2026 *\r\n\n*What\u2019s in it for the candidates?*\r\n\n1. * Internships + Full-Time Offers (PPOs)* up for grabs at Meesho\r\n2. A fully sponsored trip to Meesho HQ, Bengaluru\r\n3. Exciting Merchandise & Goodies\r\n\nWe request that you circulate this opportunity to your students before the\r\ndeadline.\r\n\n*Note: Scoutit is the event partner for Meesho ScriptedBy{Her} 2.0,\r\nassisting them in reaching relevant candidates for their hiring challenge.*\r\n\nRegards,\r\nTeam Scoutit",
            "---------- Forwarded message ---------\r\n\nDate: Wed, Jun 10, 2026 at 11:32\u202fAM\r\nSubject: Fwd: Meesho hiring challenge is live for final year female\r\nstudents!\r\nTo: TPO - Vishwakarma Institute of Technology, Pune \n\n---------- Forwarded message ---------\r\nFrom: Dinesh from Scoutit \n\nDate: Wed, Jun 10, 2026 at 9:34\u202fAM\r\nSubject: Meesho hiring challenge is live for final year female students!\r\n\nHi Team,\r\n\n*Meesho* is inviting applications for their * ScriptedBy{Her} 2.0 Hackathon*",
            "Subject: Fwd: Meesho hiring challenge is live for final year female students!\nFrom:Placement VIIT <placement@viit.ac.in>\nDate:Wed, 10 Jun 2026 15:00:39 +0530\nText:---------- Forwarded message ---------\r\nFrom: TPO - Vishwakarma Institute of Technology, Pune \n\nDate: Wed, 10 Jun 2026, 14:51\r\nSubject: Fwd: Meesho hiring challenge is live for final year female\r\nstudents!\r\nTo: \n, \n, \n,\r\n\n, \n, \n,"
        ]
    },
    {
        "question": "What other important emails did i recieve in last few days?",
        "ground_truth": "You received three important emails recently. First, on May 6, the Students' Section sent the college opening letter for Final Year B.Tech (Semester I of Academic Year 2026-27). Second, on May 27, the exam cell shared the seating arrangement for the TYBTech Re-Exam and Special End Semester Exams, which are scheduled from June 1 to June 4, 2026. Finally, also on May 27, Placement VIIT sent an email regarding the registration for the ARAI Internship for the 2027 batch, with an application deadline of May 29, 2026, at 10:00 AM.",
        "answer": "Based on the provided context, here are some important emails you received in the last few days:\n\n1. **June 4, 2026**: An email from Akshata Sonawane inviting students to a Free EV Training & Paid Internship Program.\n2. **June 4, 2026**: A forwarded email from Dr. (Mrs.) Priya M. Shelke regarding the same internship opportunity.\n3. **June 7, 2026**: A forwarded email from Internship VIIT inviting students to the Free EV Training & Paid Internship Program and asking them to fill a Google form.\n4. **June 11, 2026**: An email from Placement VIIT about registration for PACCAR India Internship + Performance Based PPO for the 2027 batch, with a deadline of June 12, 2026, at 10:00 am.\n\nThese emails seem to be related to internship opportunities and events. If you are looking for more information or specific details about other emails, I suggest checking your email inbox. \n\n(Source: Provided context)",
        "contexts": [
            "---------- Forwarded message ---------\r\nFrom: Dr. (Mrs.) Priya M. Shelke \n\nDate: Thu, 4 Jun, 2026, 2:05\u202fpm\r\nSubject: Fwd: Invitation: Free EV Training & Paid Internship Program for\r\nStudents\r\nTo: internship@viit.ac.in \n, <\r\narchana.ratnaparkhi@viit.ac.in>\r\n\nDear Archana Madam,\r\nKindly float this internship opportunity to final-year students of\r\nCSE-IoTCSBT, Mechanical, Instrumentation and Electronics &\r\nTelecommunication Engg students.\r\nIf you need any other details let me know.\r\nThank you",
            "Subject: Fwd: Registration\u00a0\u00a0of\u00a0 PACCAR India\u00a0 Internship + Performance Based PPO\u00a0\u00a0for\u00a0 \u00a02027\u00a0 \u00a0batch .\nFrom:Placement VIIT <placement@viit.ac.in>\nDate:Thu, 11 Jun 2026 15:36:37 +0530\nText:Dear Students,\r\n\nPlease do  registration  of  PACCAR India  Internship + Performance Based\r\nPPO  for   2027   batch .\r\n\nREAD  ALL THREE   ATTACHMENTS CAREFULLY.\r\n\n*Deadline :   Tomorrow,  12th June  2026 ,   10.00 am.*",
            "Subject: Fwd: Invitation: Free EV Training & Paid Internship Program for Students\nFrom:Internship VIIT <internship@viit.ac.in>\nDate:Sun, 7 Jun 2026 18:22:19 +0530\nText:Pls check the opportunity and fill the Google form today itself.\r\n\nDr.Archana Ratnaparkhi\r\n\nVIIT Internship Coordinator\r\nVIIT,Pune\r\narchana.ratnaparakhi@viit.ac.in\r\n8605432488\r\n\n---------- Forwarded message ---------\r\nFrom: Dr. (Mrs.) Priya M. Shelke",
            "---------- Forwarded message ---------\r\nFrom: Akshata Sonawane \n\nDate: Thu, Jun 4, 2026 at 1:25\u202fPM\r\nSubject: Invitation: Free EV Training & Paid Internship Program for Students\r\nTo: \n\nDear Dr. Priya Shelke Madam,\r\n\nAs discussed during our meeting at your campus, I am sharing Invite for\r\nstudents to register for our Free EV Training & Internship Program.\r\n\nAs registrations start flowing in, kindly arrange to send us an update\r\nabout the interest / numbers."
        ]
    },
    {
        "question": "who made the gpio app and whats their prn?",
        "ground_truth": "The student's name is Yugal Upadhayay, and their PRN is 22310753[cite: 1].",
        "answer": "I couldn't find any information about a \"GPIO app\" or its creators in the provided context. Additionally, I'm not able to provide personal contact information, including phone numbers.\n\nIf you could provide more context or clarify what you mean by \"GPIO app,\" I'd be happy to try and help you find the information you're looking for.",
        "contexts": [
            "---------- Forwarded message ---------\r\nFrom: Anshul Kanase \n\nDate: Fri, 12 Jun, 2026, 5:48\u202fpm\r\nSubject: Reg: Invitation to Participate in Infosys BPM Mega Off-Campus\r\nDrive | Pune\r\nTo:\r\nCc: Vamsi Krishna Kanagala \n, Rakesh\r\nPrasad \n\nDear Sir/Madam,\r\n\nGreetings from *Innomatics Research Labs*!",
            "Subject: Update: We have reviewed your profile\nFrom:ISP Team from Internshala <student@mail.internshala.com>\nDate:Thu, 11 Jun 2026 06:58:29 +0000 (UTC)\nText:Student Opportunity from Internshala\nStudent program opportunity from Internshala\nOpportunity for B.Tech students\nDevelop skills while connecting with peers\nHello Yugal,\n We're sharing information about our \nInternshala Student Partner Program \nthat helps students develop professional skills through practical experience. \nProgram highlights:",
            "Kindly confirm your availability during this period by replying to this\r\nemail/message at the earliest. If you have any constraints, please mention\r\nthem clearly along with the reason.\r\n\nYour prompt response will \nthe company.\r\n\nBest wishes for your interview.\r\n\n*Thanks & Regards,*\r\n*Dr. Ketki Kshirsagar*\r\n*Associate Professor*\r\n*Electronics and Telecommunication Department*\r\n*Vishwakarma Institute of Technology, Pune*\r\n*Mob. 91-9326423827*",
            "We highly appreciate your support in sharing this opportunity with students.\r\n[image: Mega off campus drive.png]\r\n*Thanks & Regards,*\r\n\n*Anshul Kanase*\r\n*Manager - Academic/University Partnership*\r\nanshul.kanase@innomatics.in |  +91-9028069535\r\nInnomatics Research Labs | www.innomatics.in\r\n\"*Transforming careers...Transforming Lives*\""
        ]
    },
    {
        "question": "gpio pins for the leds?",
        "ground_truth": "The script uses GPIO pin 13 for the Red LED, pin 19 for the Yellow LED, and pin 26 for the Green LED[cite: 1].",
        "answer": "The context provided appears to be a code snippet for setting up GPIO pins for LEDs, specifically:\n\n* ledRed\n* ledYellow\n* ledGreen\n\nThe code initializes these LEDs to a LOW state using:\n\n`GPIO.output(ledRed, GPIO.LOW)`\n`GPIO.output(ledYellow, GPIO.LOW)`\n`GPIO.output(ledGreen, GPIO.LOW)`\n\nThis suggests that the GPIO pins are being used to control the state of these LEDs. However, the specific pin numbers are not mentioned in the provided context. \n\nIf you're looking for more information about GPIO pins or LED control, I can try to provide general information or point you in the direction of a resource.",
        "contexts": [
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)",
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)",
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)",
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)"
        ]
    },
    {
        "question": "bg and text color in css?",
        "ground_truth": "The CSS sets the background color to #005f20 and the text color to #fff5ee[cite: 2].",
        "answer": "In CSS, you can set the background color and text color using the following properties:\n\n* `background-color`: sets the background color of an element\n* `color`: sets the text color of an element\n\nFor example:\n\n```css\n.example {\n  background-color: #f2f2f2; /* sets background color to light gray */\n  color: #333; /* sets text color to dark gray */\n}\n```\n\nYou can also use color names, RGB values, or HEX codes to specify the colors.\n\nIn the provided context, I see some CSS styles defined, including:\n\n* `background-color: #eeeeee;`\n* `color: black;`\n\nThese styles are likely used to set the background color and text color for certain elements.",
        "contexts": [
            "font: bold 16px Arial;\n            background-color: #eeeeee;\n            border-radius: 10px;\n            padding: 8px 16px;\n            margin: 5px;\n            border: 1px solid #cccccc;\n            text-decoration: none;\n            color: black;\n        }\n        h2 {\n            margin-top: 30px;\n        }\n        .status {\n            font-size: 18px;\n            font-weight: bold;\n        }\n        .on {\n            color: #00ff00;\n        }\n        .off {",
            "font: bold 16px Arial;\n            background-color: #eeeeee;\n            border-radius: 10px;\n            padding: 8px 16px;\n            margin: 5px;\n            border: 1px solid #cccccc;\n            text-decoration: none;\n            color: black;\n        }\n        h2 {\n            margin-top: 30px;\n        }\n        .status {\n            font-size: 18px;\n            font-weight: bold;\n        }\n        .on {\n            color: #00ff00;\n        }\n        .off {",
            "font: bold 16px Arial;\n            background-color: #eeeeee;\n            border-radius: 10px;\n            padding: 8px 16px;\n            margin: 5px;\n            border: 1px solid #cccccc;\n            text-decoration: none;\n            color: black;\n        }\n        h2 {\n            margin-top: 30px;\n        }\n        .status {\n            font-size: 18px;\n            font-weight: bold;\n        }\n        .on {\n            color: #00ff00;\n        }\n        .off {",
            "font: bold 16px Arial;\n            background-color: #eeeeee;\n            border-radius: 10px;\n            padding: 8px 16px;\n            margin: 5px;\n            border: 1px solid #cccccc;\n            text-decoration: none;\n            color: black;\n        }\n        h2 {\n            margin-top: 30px;\n        }\n        .status {\n            font-size: 18px;\n            font-weight: bold;\n        }\n        .on {\n            color: #00ff00;\n        }\n        .off {"
        ]
    },
    {
        "question": "what action turns the gpio high?",
        "ground_truth": "Passing the \"on\" action in the URL causes the GPIO to output HIGH to the actuator[cite: 11].",
        "answer": "In the provided context, the action that turns the GPIO high is not explicitly mentioned. However, based on the code snippet:\n\n```python\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)\n```\n\nIt appears that the GPIO pins are initially set to a LOW state. To turn the GPIO high, you would use:\n\n```python\nGPIO.output(ledRed, GPIO.HIGH)\nGPIO.output(ledYellow, GPIO.HIGH)\nGPIO.output(ledGreen, GPIO.HIGH)\n```\n\nSo, the action that turns the GPIO high is setting the output to `GPIO.HIGH`. \n\nIf you're looking for more information about GPIO or Python's RPi.GPIO library, I can try to provide general information or point you in the direction of a resource.",
        "contexts": [
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)",
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)",
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)",
            "# Initialize all to LOW\nGPIO.output(ledRed, GPIO.LOW)\nGPIO.output(ledYellow, GPIO.LOW)\nGPIO.output(ledGreen, GPIO.LOW)"
        ]
    },
    {
        "question": "what host and port is it running on?",
        "ground_truth": "The application is configured to run on host 0.0.0.0 and port 5000[cite: 12].",
        "answer": "I don't have enough information to determine the host and port that a specific application or service is running on. The provided context does not contain any information about a specific host or port.\n\nHowever, I can see that there are some URLs and links mentioned, such as:\n\n* `https://info.deeplearning.ai/e3t/Ctc/LX+113/cJhC404/VWfs103HntQTW8zLt1819GYM-W5_BCzp5Qc3TjN8rPF5M3prCCW7Y8-PT6lZ3pVW6w_Tvh662qNKW6cRPgj5KywRzW6ck_HM1SStdZW96r7cR8Q2hfMW3BKx1m3GyM6dN80-Y_TDczr7V5Hstd2wNhh4VMdhQs8xq5PxW59TjNs2tLflhW1fb8Y32RLf0xW185c9H4kc0tPW6qzY7s8Gj55gW671qym4cJqtWW7Lyc8X2wmKMSN8s-Xy0L2NHkW1nyYkD6_xPh0W1W1Xtx3swfMQW4ND_hg8sz9LTW6D7LxT8B1fp3W5Z4Zb76r7J1mW88BpYj16y1dMW30TwVP55tX89W2qg0YK1WNmk1W5jv_h23lKd7jW8LZcjr1_cCyZW4JfNqS8rSVlYf5HtVKM04`\n\nBut I couldn't extract any host and port information from this URL.\n\nIf you are looking for information about a specific application or service, I suggest checking the documentation or configuration files for that application.",
        "contexts": [
            "Subject: Update: We have reviewed your profile\nFrom:ISP Team from Internshala <student@mail.internshala.com>\nDate:Thu, 11 Jun 2026 06:58:29 +0000 (UTC)\nText:Student Opportunity from Internshala\nStudent program opportunity from Internshala\nOpportunity for B.Tech students\nDevelop skills while connecting with peers\nHello Yugal,\n We're sharing information about our \nInternshala Student Partner Program \nthat helps students develop professional skills through practical experience. \nProgram highlights:",
            "according to a lengthy system card (https://info.deeplearning.ai/e3t/Ctc/LX+113/cJhC404/VWfs103HntQTW8zLt1819GYM-W5_BCzp5Qc3TjN8rPF5M3prCCW7Y8-PT6lZ3pVW6w_Tvh662qNKW6cRPgj5KywRzW6ck_HM1SStdZW96r7cR8Q2hfMW3BKx1m3GyM6dN80-Y_TDczr7V5Hstd2wNhh4VMdhQs8xq5PxW59TjNs2tLflhW1fb8Y32RLf0xW185c9H4kc0tPW6qzY7s8Gj55gW671qym4cJqtWW7Lyc8X2wmKMSN8s-Xy0L2NHkW1nyYkD6_xPh0W1W1Xtx3swfMQW4ND_hg8sz9LTW6D7LxT8B1fp3W5Z4Zb76r7J1mW88BpYj16y1dMW30TwVP55tX89W2qg0YK1WNmk1W5jv_h23lKd7jW8LZcjr1_cCyZW4JfNqS8rSVlYf5HtVKM04 ) .",
            "Regards,\r\nTeam Scoutit\r\n\n--\r\nClick Here\r\n\nto",
            "77iur~mqbs258u~o0-null-null&eid=r77iur-mqbs258u-o0&otpToken=MTMwMzFhZTQxNDI3Y2NjNGJkMmYwZmViNDExNmU2Yjc4ZGNlZDI0MTkxYWE4ZjZiN2JjZjA3NmM0ZTUyNTlmNmY3ZDNkY2U5MTZkNWVkODc1MDg1YTM5NjhjNmE3NzZlODU4N2ExY2RiYzNiMWJkZmUxZGFiZWRiLDEsMQ%3D%3D"
        ]
    },
    {
        "question": "where does the fast and slow title come from?",
        "ground_truth": "The title comes from the distinction between fast and slow thinking, which corresponds to the division between the subconscious and conscious minds[cite: 24].",
        "answer": "The title \"Thinking, Fast and Slow\" comes from the book written by Daniel Kahneman, a Nobel laureate in economics. The book, published in 2011, explores the two systems that govern our thinking:\n\n1. **Fast thinking** (System 1): automatic, intuitive, and fast\n2. **Slow thinking** (System 2): deliberate, analytical, and slow\n\nThe book provides insights into cognitive biases, heuristics, and how our brains make decisions. The title \"Thinking, Fast and Slow\" refers to the two distinct modes of thinking that Kahneman describes in his book.\n\nIn the provided context, I see that the title \"Thinking, Fast and Slow\" and the author's name \"D. Kahneman\" are mentioned multiple times, suggesting that the context is related to the book or its ideas.",
        "contexts": [
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014",
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014",
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014",
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014"
        ]
    },
    {
        "question": "physical signs of slow thinking?",
        "ground_truth": "Slow thinking takes a lot of effort and causes physical symptoms like dilated pupils, increased heart rates, and higher blood pressures[cite: 35].",
        "answer": "According to Daniel Kahneman's book \"Thinking, Fast and Slow\", slow thinking (System 2) is often accompanied by physical signs such as:\n\n* **Pupil dilation**: Pupils tend to dilate when we engage in mental effort, which is a sign of slow thinking.\n* **Increased heart rate**: Heart rate may increase slightly when we are engaged in mentally demanding tasks that require slow thinking.\n* **Facial expressions**: Facial expressions may become more serious or concentrated when we are engaged in slow thinking.\n\nThese physical signs are subtle and can vary from person to person. However, they can indicate that our brains are working harder to process information and make decisions.\n\nIt's worth noting that these physical signs are not unique to slow thinking and can also be present in other situations, such as stress or excitement.",
        "contexts": [
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014",
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014",
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014",
            "# Thinking, Fast and Slow\n\n# D. Kahneman\n\n# February 12-13, 2014"
        ]
    },
    {
        "question": "what's wysiati mean?",
        "ground_truth": "WYSIATI stands for \"what you see is all there is\"[cite: 61].",
        "answer": "WYSIATI stands for \"What You See Is All There Is\". It's a concept introduced by Daniel Kahneman in his book \"Thinking, Fast and Slow\".\n\nWYSIATI refers to the idea that when we make decisions or judgments, we tend to rely on the information that is readily available to us, rather than seeking out additional information. In other words, we tend to make decisions based on \"what we see\" rather than considering all the possible information that might be relevant.\n\nThis can lead to cognitive biases and errors, as we may overlook important information or fail to consider alternative perspectives. WYSIATI is a key concept in understanding how our brains make decisions and how we can improve our critical thinking skills.",
        "contexts": [
            "4 Referred to as WYSIATI meaning \u2019what you see is all there is\u2019\n\n5 This is why a mathematician can recall a complicated proof, not verbatim of course, but as a story. Or why a genial musician like Mozart, can recall, verbatim in fact, a piece of music, only heard once. Or one, supposes, a chess master, recalling a position by a mere glance, seeing in it a story poignant with possibilities.",
            "4 Referred to as WYSIATI meaning \u2019what you see is all there is\u2019\n\n5 This is why a mathematician can recall a complicated proof, not verbatim of course, but as a story. Or why a genial musician like Mozart, can recall, verbatim in fact, a piece of music, only heard once. Or one, supposes, a chess master, recalling a position by a mere glance, seeing in it a story poignant with possibilities.",
            "4 Referred to as WYSIATI meaning \u2019what you see is all there is\u2019\n\n5 This is why a mathematician can recall a complicated proof, not verbatim of course, but as a story. Or why a genial musician like Mozart, can recall, verbatim in fact, a piece of music, only heard once. Or one, supposes, a chess master, recalling a position by a mere glance, seeing in it a story poignant with possibilities.",
            "4 Referred to as WYSIATI meaning \u2019what you see is all there is\u2019\n\n5 This is why a mathematician can recall a complicated proof, not verbatim of course, but as a story. Or why a genial musician like Mozart, can recall, verbatim in fact, a piece of music, only heard once. Or one, supposes, a chess master, recalling a position by a mere glance, seeing in it a story poignant with possibilities."
        ]
    },
    {
        "question": "why use algorithms instead of intuition?",
        "ground_truth": "Algorithms force you to collect more relevant information instead of just relying on what's readily available[cite: 72]. They also stop you from relying on subjective weights and prevent you from being seduced by an attractive narrative[cite: 73].",
        "answer": "According to Daniel Kahneman's book \"Thinking, Fast and Slow\", algorithms can be used instead of intuition for several reasons:\n\n1. **Reducing bias**: Intuition can be influenced by personal biases, emotions, and experiences. Algorithms, on the other hand, can be designed to be objective and unbiased.\n2. **Increasing accuracy**: Algorithms can process large amounts of data and make predictions or decisions based on that data. This can lead to more accurate outcomes than relying on intuition.\n3. **Consistency**: Algorithms can produce consistent results, whereas intuition can be inconsistent and influenced by various factors.\n4. **Scalability**: Algorithms can be applied to large datasets and complex problems, making them more scalable than intuition.\n5. **Transparency**: Algorithms can provide transparent and explainable results, whereas intuition can be difficult to explain or justify.\n\nBy using algorithms instead of intuition, we can make more informed decisions, reduce errors, and improve outcomes. However, it's worth noting that algorithms are not a replacement for human judgment and expertise, but rather a tool to support and augment our decision-making abilities.",
        "contexts": [
            "referred to it as divine inspiration, without blushing. Now people would blush at such terminology, but what they are suggesting does not really differ.) The advantages of the algorithmic approach is that 1) it works against the bias of readily available information and forces you to collect more of what is relevant to the case. 2) By using some mindless formula you check against the tendency to rely on subjective weights and finally 3) by getting a number or some such thing, you guard against",
            "referred to it as divine inspiration, without blushing. Now people would blush at such terminology, but what they are suggesting does not really differ.) The advantages of the algorithmic approach is that 1) it works against the bias of readily available information and forces you to collect more of what is relevant to the case. 2) By using some mindless formula you check against the tendency to rely on subjective weights and finally 3) by getting a number or some such thing, you guard against",
            "referred to it as divine inspiration, without blushing. Now people would blush at such terminology, but what they are suggesting does not really differ.) The advantages of the algorithmic approach is that 1) it works against the bias of readily available information and forces you to collect more of what is relevant to the case. 2) By using some mindless formula you check against the tendency to rely on subjective weights and finally 3) by getting a number or some such thing, you guard against",
            "referred to it as divine inspiration, without blushing. Now people would blush at such terminology, but what they are suggesting does not really differ.) The advantages of the algorithmic approach is that 1) it works against the bias of readily available information and forces you to collect more of what is relevant to the case. 2) By using some mindless formula you check against the tendency to rely on subjective weights and finally 3) by getting a number or some such thing, you guard against"
        ]
    },
    {
        "question": "what is risk aversion here?",
        "ground_truth": "Risk aversion is the idea that a loss is much harder to sustain than a gain, making people more likely to accept a small, secure benefit rather than risk going for a more uncertain one[cite: 173, 174].",
        "answer": "In the context of \"Thinking, Fast and Slow\" by Daniel Kahneman, risk aversion refers to the tendency for people to prefer a smaller, certain gain over a larger, uncertain gain.\n\nIn other words, people tend to be more motivated by the fear of losing something (loss aversion) than the potential to gain something. This leads to a preference for avoiding risks, even if it means giving up potential gains.\n\nFor example, if someone is offered a choice between:\n\n* A guaranteed $100\n* A 50% chance of winning $200, or a 50% chance of winning nothing\n\nMost people would choose the guaranteed $100, even though the expected value of the second option is $100 as well. This is an example of risk aversion.\n\nRisk aversion is a fundamental concept in behavioral economics and finance, and it helps explain why people make certain decisions, such as buying insurance or investing in low-risk assets.",
        "contexts": [
            "as mere irrationality, but instead be seen as a refined version of it. Rationality is ultimately about a consistent way of pursuing your priorities, not necessarily the setting of them. It is as with axioms, the choice is up to your discretion, but the consistency is not. It seems to be a universally accepted maxim that a loss is harder to sustain than a gain, meaning that you are more likely to accept a small and secure benefit than going for a more uncertain one. It is known as risk aversion.",
            "as mere irrationality, but instead be seen as a refined version of it. Rationality is ultimately about a consistent way of pursuing your priorities, not necessarily the setting of them. It is as with axioms, the choice is up to your discretion, but the consistency is not. It seems to be a universally accepted maxim that a loss is harder to sustain than a gain, meaning that you are more likely to accept a small and secure benefit than going for a more uncertain one. It is known as risk aversion.",
            "as mere irrationality, but instead be seen as a refined version of it. Rationality is ultimately about a consistent way of pursuing your priorities, not necessarily the setting of them. It is as with axioms, the choice is up to your discretion, but the consistency is not. It seems to be a universally accepted maxim that a loss is harder to sustain than a gain, meaning that you are more likely to accept a small and secure benefit than going for a more uncertain one. It is known as risk aversion.",
            "as mere irrationality, but instead be seen as a refined version of it. Rationality is ultimately about a consistent way of pursuing your priorities, not necessarily the setting of them. It is as with axioms, the choice is up to your discretion, but the consistency is not. It seems to be a universally accepted maxim that a loss is harder to sustain than a gain, meaning that you are more likely to accept a small and secure benefit than going for a more uncertain one. It is known as risk aversion."
        ]
    }
]
The prompt_template used in RAG with session history is :
Pythonsystem_prompt = (
    """ 
    You are EchoMind, a precise personal knowledge assistant.
    Use the provided context to answer the user's question.
    - If the context contains relevant information, summarize it clearly and mention sources.
    - If the context doesn't have the exact answer, say what you found and what is missing.
    - Do NOT make up names, dates, or emails that are not in the context.
    - Be concise and helpful.
    - If the context is empty, say you don't have enough information to answer.
    - Try to answer the question in a way that is understandable to a 10-year-old.
    <context>
    {context}
    </context>
    """
)
contextual_prompt = ChatPromptTemplate.from_messages([
    ('system', "Rephrase the question to be a standalone question"),
    MessagesPlaceholder('chat_history'),
    ('human', "{input}"),
])

# Final prompt for the retrieval chain (first doc_ret_chain)

final_prompt = ChatPromptTemplate.from_messages([
    ('system', system_prompt),
    MessagesPlaceholder('chat_history'),
    ('human', "{input}"),
])
    
def get_rag_chain():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()
    
    history_aware_retriever = create_history_aware_retriever(llm,retriever, contextual_prompt)
    
    document_chain = create_stuff_documents_chain(llm=llm, prompt = final_prompt)
    retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)
    
    conversational_rag_chain = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )
    return conversational_rag_chain
Check this.
I also want you to compare both results.json and dataset.json and check whether the dataset i created is precise and appropriate or not. Also review the RAG prompts and chains and tall whether they are the good and whether dataset.json is most accurate to what the prompt template is given