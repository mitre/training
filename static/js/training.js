/*

Data object & functions to be used by Alpine.js x-data in training.html

*/

function trainingData() {
  return {
    /*
    Variables
    */
    selectedCert: '',
    selectedBadge: '',
    badgeList: [],
    visibleFlagList: [],
    completedFlags: 0,
    completedBadges: 0,
    flagList: [],
    completedCertificate: false,
    certificateCodeList: [],
    certificateCode: '',
    refresher: null,

    /*
        Functions
        */
    getEmptyDataObject() {
      return {
        flagList: [],
        badgeList: [],
        completedFlags: 0,
        completedBadges: 0,
        certificateCodeList: [],
      };
    },

    /*
    updateVisibleFlags() is called by $watch in training.html, when the
    variable selectedBadge is updated,
    and updates the list of visible flags as well
    */
    updateVisibleFlags(badge) {
      if (badge) {
        this.selectedBadge = badge;
        this.visibleFlagList = this.flagList.filter(
          (flag) => flag.badge_name === this.selectedBadge.name,
        );
      } else this.visibleFlagList = this.flagList;
    },

    /*
    Check if certificate is complete, and generate code if completed
    */
    checkCertificateCompletion() {
      if (this.completedBadges === this.badgeList.length) {
        this.completedCertificate = true;
        let code = this.certificateCodeList.sort(
          (a, b) => a.toString().length - b.toString().length,
        );
        code = code.join(' ');
        this.certificateCode = btoa(code);
        this.confetti();
      }
    },

    compareFlags(currentBadge, iconSrc, flag, flagIndex) {
      const updatedFlag = {
        ...flag,
        badge_name: currentBadge.name,
        badge_icon: iconSrc,
        cert_name: this.selectedCert,
        showMore: false,
      };
      if (this.flagList[flagIndex]) {
        const previousFlag = this.flagList[flagIndex];
        if (previousFlag.name == updatedFlag.name) {
          updatedFlag.showMore = previousFlag.showMore;
        }
      }
      return updatedFlag;
    },

    updateFlagData(newData) {
      if (newData) {
        this.flagList = newData.flagList;
        this.badgeList = newData.badgeList;
        this.completedFlags = newData.completedFlags;
        this.completedBadges = newData.completedBadges;
        this.certificateCodeList = newData.certificateCodeList;
      }
    },

    async getFlags(data) {
      if (!data) return;
      const newData = this.getEmptyDataObject();
      let runningFlagIndex = 0;

      // Fetch flag from API and compares it to previous data,
      // rather than completely override (for variables like showMore)
      data.badges.forEach((badge) => {
        const iconSrc = `/training/img/badges/${badge.name}.png`;
        let isBadgeCompleted = false;
        let badgeCompletedFlags = 0;

        badge.flags.forEach((flag) => {
          const currentFlag = this.compareFlags(badge, iconSrc, flag, runningFlagIndex);
          if (currentFlag.completed) badgeCompletedFlags += 1;
          newData.flagList.push(currentFlag);
          newData.certificateCodeList.push(currentFlag.code);
          runningFlagIndex += 1;
        });

        if (badgeCompletedFlags === badge.flags.length) {
          newData.completedBadges += 1;
          isBadgeCompleted = true;
        }

        newData.badgeList.push({ ...badge, completed: isBadgeCompleted, icon_src: iconSrc });
        // Keep selected badge so it doesn't get overriden by new data
        if (this.selectedBadge.name === badge.name) this.selectedBadge = badge;
        newData.completedFlags += badgeCompletedFlags;
      });
      this.updateFlagData(newData);
    },

    /*
        getTraining() makes call to get flags, and if successful, does the following:
        1) sets a refresher() to fetch flags again after set interval
        2) check if certificate is complete
        3) updates visibleFlagList
    */
    getTraining(selectedCert) {
      if (this.refresher) clearInterval(this.refresher);
      this.selectedCert = selectedCert;
      fetch('/plugin/training/flags', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.selectedCert, answers: {},
        }),
      })
        .then((r) => {
          if (r.ok) return r.json();
          return console.error('Fetch error:', r);
        }).then((data) => {
          this.getFlags(data)
            .then(() => {
              this.refresher = setInterval(() => this.getTraining(this.selectedCert), 15000);
              this.updateVisibleFlags(this.selectedBadge);
              this.checkCertificateCompletion();
            });
          return true;
        }).catch((e) => console.error(e));
    },

    copyCode() {
      document.getElementById('certificate-code').select();
      document.execCommand('copy');
      document.getElementById('copy-text').innerHTML = 'Copied!';
    },

    // Source: https://github.com/catdad/canvas-confetti
    confetti() {
      const canvas = document.getElementById('canvas');

      const confettiCanon = confetti.create(canvas, {
        resize: true,
        useWorker: true
      });
      // do this for 30 seconds
      var duration = 30 * 1000;
      var end = Date.now() + duration;

      (function frame() {
        // launch a few confetti from the left edge
        confetti({
          particleCount: 7,
          angle: 60,
          spread: 55,
          origin: { x: 0 }
        });
        // and launch a few from the right edge
        confetti({
          particleCount: 7,
          angle: 120,
          spread: 55,
          origin: { x: 1 }
        });

        // keep going until we are out of time
        if (Date.now() < end) {
          requestAnimationFrame(frame);
        }
      }());
    }
  };
}
