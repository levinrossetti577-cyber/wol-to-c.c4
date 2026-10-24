package de.catgirlwolf.client;

import de.catgirlwolf.CatgirlWolf;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.renderer.entity.state.WolfRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;

/**
 * Spielergroßes Catgirl-Modell im Standard-Spielerskin-Layout (64x64, schmale Arme).
 * Jeder normale Minecraft-Skin funktioniert als Textur. Ohren und Schwanz lesen ihre Pixel
 * aus den Haarbereichen des Kopfes (Seite bzw. Rückseite) und haben so automatisch die Haarfarbe.
 * Animationen sind prozedural, damit keine zusätzliche Animationsbibliothek nötig ist.
 *
 * Hierarchie: torso (Pivot an der Hüfte) -> head -> Ohren | Schwanz (3 Glieder), Arme
 *             right_leg/left_leg (Oberschenkel) -> right_shin/left_shin (Unterschenkel mit Kniegelenk)
 *
 * Diese Datei wurde aus derselben Definition erzeugt wie die Textur (tools/spec_skin.py).
 */
public class CatgirlWolfModel extends EntityModel<WolfRenderState> {
	public static final ModelLayerLocation LAYER =
			new ModelLayerLocation(Identifier.fromNamespaceAndPath(CatgirlWolf.MOD_ID, "catgirl_wolf"), "main");

	private static final float PI = Mth.PI;

	private final ModelPart torso, head, leftEar, rightEar;
	private final ModelPart tail, tailMid, tailTip, rightArm, leftArm;
	private final ModelPart rightLeg, rightShin, leftLeg, leftShin;

	public CatgirlWolfModel(ModelPart root) {
		super(root);
		this.torso = root.getChild("torso");
		this.head = torso.getChild("head");
		this.leftEar = head.getChild("left_ear");
		this.rightEar = head.getChild("right_ear");
		this.tail = torso.getChild("tail");
		this.tailMid = tail.getChild("tail_mid");
		this.tailTip = tailMid.getChild("tail_tip");
		this.rightArm = torso.getChild("right_arm");
		this.leftArm = torso.getChild("left_arm");
		this.rightLeg = root.getChild("right_leg");
		this.rightShin = rightLeg.getChild("right_shin");
		this.leftLeg = root.getChild("left_leg");
		this.leftShin = leftLeg.getChild("left_shin");
	}

	public static LayerDefinition createBodyLayer() {
		MeshDefinition mesh = new MeshDefinition();
		PartDefinition root = mesh.getRoot();
		PartDefinition torso = root.addOrReplaceChild("torso", CubeListBuilder.create()
				.texOffs(16, 16).addBox(-4f, -12f, -2f, 8f, 12f, 4f, CubeDeformation.NONE)
				.texOffs(16, 32).addBox(-4f, -12f, -2f, 8f, 12f, 4f, new CubeDeformation(0.25f)),
				PartPose.offset(0f, 12f, 0f));
		PartDefinition head = torso.addOrReplaceChild("head", CubeListBuilder.create()
				.texOffs(0, 0).addBox(-4f, -8f, -4f, 8f, 8f, 8f, CubeDeformation.NONE)
				.texOffs(32, 0).addBox(-4f, -8f, -4f, 8f, 8f, 8f, new CubeDeformation(0.5f)),
				PartPose.offset(0f, -12f, 0f));
		PartDefinition leftear = head.addOrReplaceChild("left_ear", CubeListBuilder.create()
				.texOffs(0, 8).addBox(-1.5f, -3f, -0.5f, 3f, 3f, 1f, CubeDeformation.NONE),
				PartPose.offset(2.6f, -8.3f, -0.5f));
		PartDefinition rightear = head.addOrReplaceChild("right_ear", CubeListBuilder.create()
				.texOffs(0, 8).addBox(-1.5f, -3f, -0.5f, 3f, 3f, 1f, CubeDeformation.NONE),
				PartPose.offset(-2.6f, -8.3f, -0.5f));
		PartDefinition tail = torso.addOrReplaceChild("tail", CubeListBuilder.create()
				.texOffs(24, 8).addBox(-0.5f, 0f, -0.5f, 1f, 5f, 1f, CubeDeformation.NONE),
				PartPose.offset(0f, -1.5f, 2.4f));
		PartDefinition tailmid = tail.addOrReplaceChild("tail_mid", CubeListBuilder.create()
				.texOffs(28, 8).addBox(-0.5f, 0f, -0.5f, 1f, 5f, 1f, new CubeDeformation(-0.05f)),
				PartPose.offset(0f, 4.8f, 0f));
		PartDefinition tailtip = tailmid.addOrReplaceChild("tail_tip", CubeListBuilder.create()
				.texOffs(24, 9).addBox(-0.5f, 0f, -0.5f, 1f, 4f, 1f, new CubeDeformation(-0.1f)),
				PartPose.offset(0f, 4.8f, 0f));
		PartDefinition rightarm = torso.addOrReplaceChild("right_arm", CubeListBuilder.create()
				.texOffs(40, 16).addBox(-1.5f, -2f, -2f, 3f, 12f, 4f, CubeDeformation.NONE)
				.texOffs(40, 32).addBox(-1.5f, -2f, -2f, 3f, 12f, 4f, new CubeDeformation(0.25f)),
				PartPose.offset(-5f, -10f, 0f));
		PartDefinition leftarm = torso.addOrReplaceChild("left_arm", CubeListBuilder.create()
				.texOffs(32, 48).addBox(-1.5f, -2f, -2f, 3f, 12f, 4f, CubeDeformation.NONE)
				.texOffs(48, 48).addBox(-1.5f, -2f, -2f, 3f, 12f, 4f, new CubeDeformation(0.25f)),
				PartPose.offset(5f, -10f, 0f));
		PartDefinition rightleg = root.addOrReplaceChild("right_leg", CubeListBuilder.create()
				.texOffs(0, 16).addBox(-2f, 0f, -2f, 4f, 6f, 4f, CubeDeformation.NONE)
				.texOffs(0, 32).addBox(-2f, 0f, -2f, 4f, 6f, 4f, new CubeDeformation(0.25f)),
				PartPose.offset(-1.9f, 12f, 0f));
		PartDefinition rightshin = rightleg.addOrReplaceChild("right_shin", CubeListBuilder.create()
				.texOffs(0, 22).addBox(-2f, 0f, -2f, 4f, 6f, 4f, new CubeDeformation(-0.02f))
				.texOffs(0, 38).addBox(-2f, 0f, -2f, 4f, 6f, 4f, new CubeDeformation(0.23f)),
				PartPose.offset(0f, 6f, 0f));
		PartDefinition leftleg = root.addOrReplaceChild("left_leg", CubeListBuilder.create()
				.texOffs(16, 48).addBox(-2f, 0f, -2f, 4f, 6f, 4f, CubeDeformation.NONE)
				.texOffs(0, 48).addBox(-2f, 0f, -2f, 4f, 6f, 4f, new CubeDeformation(0.25f)),
				PartPose.offset(1.9f, 12f, 0f));
		PartDefinition leftshin = leftleg.addOrReplaceChild("left_shin", CubeListBuilder.create()
				.texOffs(16, 54).addBox(-2f, 0f, -2f, 4f, 6f, 4f, new CubeDeformation(-0.02f))
				.texOffs(0, 54).addBox(-2f, 0f, -2f, 4f, 6f, 4f, new CubeDeformation(0.23f)),
				PartPose.offset(0f, 6f, 0f));
		return LayerDefinition.create(mesh, 64, 64);
	}

	@Override
	public void setupAnim(WolfRenderState s) {
		super.setupAnim(s); // setzt alle Teile auf die Grundpose zurück

		final float age = s.ageInTicks;
		final float ws = Math.min(s.walkAnimationSpeed, 1.0F);
		final float wp = s.walkAnimationPos;
		final float yaw = s.yRot * Mth.DEG_TO_RAD;
		final float pitch = s.xRot * Mth.DEG_TO_RAD;
		final float breath = Mth.sin(age * 0.08F);
		final float sway = Mth.sin(age * 0.12F);
		final boolean sitting = s.isSitting;
		final boolean dying = s.deathTime > 0.0F;

		if (sitting) {
			// Sitzpose nach Referenzbild: kniend, Knie nach vorn, Unterschenkel seitlich nach außen,
			// Hände vor dem Körper am Boden, Oberkörper leicht nach vorn geneigt, Kopf schief.
			torso.y = 21.8F;
			torso.xRot = 0.30F + breath * 0.015F;
			head.xRot = pitch - 0.16F;
			head.yRot = yaw;
			head.zRot = 0.14F;
			sitLeg(rightLeg, rightShin, rightArm, -1.0F, breath);
			sitLeg(leftLeg, leftShin, leftArm, 1.0F, breath);
			tail.xRot = -0.15F;
			tail.yRot = 0.75F + sway * 0.08F;
			tailMid.xRot = 0.85F;
			tailMid.yRot = sway * 0.12F;
			tailTip.xRot = 0.8F;
			tailTip.yRot = sway * 0.18F;
		} else {
			// Stehen / Gehen / Rennen: Amplitude wächst mit der Geschwindigkeit
			// Werte explizit setzen, damit nach dem Aufstehen nichts von der Sitzpose übrig bleibt
			torso.y = 12.0F;
			torso.xRot = 0.15F * ws + breath * 0.012F;
			head.xRot = pitch;
			head.yRot = yaw;
			head.zRot = 0.0F;
			float ph = wp * 0.6662F;
			walkLimb(rightLeg, rightShin, rightArm, ph, 0.0F, -1.0F, ws, breath);
			walkLimb(leftLeg, leftShin, leftArm, ph, PI, 1.0F, ws, breath);
			tail.xRot = -0.85F + 0.35F * ws;
			tail.yRot = sway * 0.35F + Mth.cos(ph) * 0.35F * ws;
			tailMid.xRot = 0.95F - 0.5F * ws;
			tailMid.yRot = Mth.sin(age * 0.12F - 0.8F) * 0.3F;
			tailTip.xRot = 0.7F - 0.4F * ws;
			tailTip.yRot = Mth.sin(age * 0.12F - 1.6F) * 0.3F;
		}

		// Kopf schief legen beim Betteln (Vanilla-Wert des Wolfs)
		head.zRot += s.headRollAngle;

		// Ohren: leicht nach außen geneigt, zucken alle ~5 Sekunden kurz
		float t = age % 97.0F;
		float flick = t < 7.0F ? Mth.sin(t / 7.0F * PI) * 0.35F : 0.0F;
		leftEar.zRot = 0.2F;
		rightEar.zRot = -0.2F;
		leftEar.xRot = -flick;
		rightEar.xRot = 0.0F;

		boolean hurt = s.hasRedOverlay;
		if (s.isAngry || hurt || dying) {
			// Ohren angelegt
			leftEar.xRot = rightEar.xRot = -0.65F;
			leftEar.zRot = 0.55F;
			rightEar.zRot = -0.55F;
		}
		if (s.isAngry && !sitting) {
			tail.xRot = -0.25F; // Schwanz gesträubt nach hinten
			rightArm.xRot -= 0.55F;
			leftArm.xRot -= 0.55F;
		}
		if (hurt) {
			head.xRot -= 0.3F; // Zusammenzucken
		}
		if (dying) {
			// Vanilla kippt den ganzen Körper zur Seite; hier hängen Arme und Schwanz schlaff
			rightArm.xRot = leftArm.xRot = 0.0F;
			rightArm.zRot = 0.25F;
			leftArm.zRot = -0.25F;
			tail.xRot = -1.2F;
			tailMid.xRot = tailTip.xRot = 0.1F;
		}

		// Schwanzglieder sind im Skin-Layout senkrechte Quader; +90° legt die Wurzel nach hinten
		tail.xRot += PI / 2.0F;
	}

	private static void sitLeg(ModelPart leg, ModelPart shin, ModelPart arm, float side, float breath) {
		leg.x = 1.9F * side;
		leg.y = 22.4F;
		leg.z = -0.6F;
		leg.xRot = -PI / 2.0F;
		leg.yRot = 0.22F * side;
		shin.zRot = -(PI - 0.95F) * side;
		arm.xRot = -0.78F + breath * 0.02F;
		arm.zRot = 0.16F * side;
	}

	private static void walkLimb(ModelPart leg, ModelPart shin, ModelPart arm, float ph, float off, float side,
								 float ws, float breath) {
		leg.x = 1.9F * side;
		leg.y = 12.0F;
		leg.z = 0.0F;
		leg.yRot = 0.0F;
		shin.zRot = 0.0F;
		arm.yRot = 0.0F;
		leg.xRot = Mth.cos(ph + off) * 1.1F * ws;
		shin.xRot = Math.max(0.0F, -Mth.sin(ph + off)) * ws;
		arm.xRot = Mth.cos(ph + off + PI) * 0.9F * ws - 0.1F * ws;
		arm.zRot = (0.07F + 0.025F * breath) * -side;
	}
}
