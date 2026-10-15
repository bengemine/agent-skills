# Worked examples

Read these before drafting. They anchor the voice: each shows a generic AI draft and the same message in the right voice. The people, products, and situations are made up.

## 1. Reply to a customer question about a timeline

**Generic AI draft:**
> Hi there,
> Thank you so much for your patience! I'm pleased to share that our team is currently working diligently on the final stages of this fix. We anticipate that it will be available in the near future. Please don't hesitate to reach out if you have any further questions!

**In the right voice:**
> Hi Daniel,
>
> The export fix is in testing right now. I think we'll be able to release it next Tuesday. I'll let you know once it's live.

## 2. "Have we tried this tool?" reply

**Generic AI draft:**
> Great question! I've looked into this tool and it appears to offer a robust set of features that could potentially streamline our load-testing workflow. It might be worth exploring further alongside other solutions in this space.

**In the right voice:**
> I haven't used it myself, so I can't say how it holds up yet. I had a quick look at the docs and it runs load tests from a plain script file, which would fit how we already write our tests. If we do try it, I'd start with the checkout page (it's the slowest one we have) and compare the numbers with what we see today.

## 3. Follow-up nudge

**Generic AI draft:**
> Hi, I hope this message finds you well! I just wanted to follow up on my previous email regarding my access request. Could you please provide an update at your earliest convenience? Thank you so much!

**In the right voice:**
> Hi Leena,
>
> Just checking in on the access request I sent on Monday. Let me know if you need anything else from me to approve it.

## 4. Leave / absence notice

**Generic AI draft:**
> Dear Team, I would like to inform you that I will be unavailable on Friday due to a personal commitment. I apologize for any inconvenience this may cause and will make every effort to address all outstanding items upon my return.

**In the right voice:**
> I'm off on Friday for a family wedding. I'll go through the open review comments when I'm back on Monday.

## 5. Technical how-to reply

**Generic AI draft:**
> Great question! There are several steps involved in this process. First, you will need to ensure that the default value is configured correctly. Then, you will need to utilize the appropriate helper function. Please let me know if you need further clarification!

**In the right voice:**
> To add a new setting, put its default value in `config/defaults.json` first. Then read it with `getSetting("name")` in the service that needs it.
>
> If you want a different value on your own machine, add the same key to `config/local.json`. That file isn't committed.
>
> There's a longer write-up on the team wiki: [link]
