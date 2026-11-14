import unittest
import numpy as np
from cloud_memory import ObservedCloudMemory, register_rigid, RegistrationConfig, radius


def surface(n=8000):
    rng=np.random.default_rng(17)
    x=rng.uniform(-1,1,n); y=rng.uniform(-.5,.5,n)
    z=.2*x*x+.15*y+.12*np.sin(4*x)*np.cos(3*y)
    return np.column_stack((x,y,z))


class CloudTests(unittest.TestCase):
    def test_known_transform_recovered(self):
        p=surface()
        a=.47
        r=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1.]])
        t=np.array([.3,-.2,.4]); transformed=p@r+t
        result=register_rigid(transformed,p)
        moved=transformed@np.array(result['rotation'])+result['translation']
        self.assertTrue(result['accepted'],result['reasons'])
        self.assertLess(np.sqrt(np.mean(np.sum((moved-p)**2,axis=1)))/radius(p),.03)

    def test_incompatible_shape_rejected(self):
        rng=np.random.default_rng(1)
        p=surface(); other=rng.normal(size=(3000,3))*[.3,.3,1.5]
        result=register_rigid(other,p)
        self.assertFalse(result['accepted'])

    def test_origin_translation_invariance(self):
        p=surface(3000)
        angle=.4;r=np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1.]])
        q=p@r+[.3,.1,.2]
        a=register_rigid(q,p)
        offset=np.array([8.,-5.,7.])
        b=register_rigid(q+offset,p+offset)
        self.assertEqual(a['accepted'],b['accepted'])
        np.testing.assert_allclose(a['validation_support'],b['validation_support'],atol=1e-5)
        np.testing.assert_allclose(a['rotation'],b['rotation'],atol=1e-5)

    def test_rejection_preserves_state(self):
        m=ObservedCloudMemory('V','t','da');m.update('a',1,surface())
        before=m.cloud();state=m.snapshot()
        m.update('b',2,surface(),registration={'accepted':False,'reasons':['test_rejection']})
        np.testing.assert_array_equal(m.cloud(),before);self.assertEqual(state,m.snapshot())

    def test_bounded_anchor_and_valid_transform(self):
        p=surface();m=ObservedCloudMemory('V','t','moge',views=3,points_per_view=100)
        decision=dict(accepted=True,rotation=np.eye(3).tolist(),translation=[0,0,0])
        for i in range(6):m.update(str(i),i,p,registration=decision,provenance={'observed_only':True})
        self.assertEqual(m.snapshot()['observation_keys'],['0','4','5'])
        self.assertEqual(len(m.cloud()),300)
        self.assertEqual(len(m.provenance()),3)
        copy=m.cloud();copy[:]=0;self.assertFalse(np.all(m.cloud()==0))

    def test_nonrigid_or_duplicate_invalid_no_mutation(self):
        m=ObservedCloudMemory('V','t','da');p=surface();m.update('a',1,p)
        bad=dict(accepted=True,rotation=(2*np.eye(3)).tolist(),translation=[0,0,0])
        with self.assertRaises(ValueError):m.update('b',2,p,registration=bad)
        self.assertEqual(m.snapshot()['version'],1)
        with self.assertRaises(ValueError):m.update('a',2,p,registration=bad)

    def test_configuration_and_degeneracy(self):
        with self.assertRaises(ValueError):RegistrationConfig(minimum_support=2)
        with self.assertRaises(ValueError):register_rigid(np.zeros((100,3)),surface())


if __name__=='__main__':unittest.main()
